# LessonForge: design notes

## 1. The problem, restated

We need a system that can be trusted to decide, **without a human**, whether a lesson is good enough to put in front of a learner. The lesson itself matters less than the gate in front of it. So the questions I designed around were:

1. **What does "good enough" mean for *this* learner?** Write it down as checks that clearly pass or fail.
2. **How do I make the judge trustworthy?** An LLM grading an LLM is the weakest link.
3. **What happens when the content fails?** Fix it efficiently, always stop, and never ship a failing lesson silently.
4. **How does the system get better over time** instead of making the same mistake every run?

The learner shaped every decision. A 12th-grade graduate from a non-English-medium school reads English slowly. One long sentence or one unexplained word can lose them. For this reader, readability is a *correctness* requirement, not a style preference.

---

## 2. Architecture

```
context ──► generate ──► evaluate ──pass──────────────► ship ──► learn ──► memory
   ▲                       │  ▲                                    ▲
   │                       │  └── revise ◄── fail & retries left    │
   │                       └──── fail & budget used ──► hold ───────┘
   └──────────────────────────── memory (rules, failure stats, human checks)
```

| Node | Responsibility | Why it is separate |
|---|---|---|
| **context** | Loads reference facts, rubric (+ human-added checks) and learned rules from memory | Makes every run reproducible from inputs on disk |
| **generate** | Writer LLM produces draft 1 from a strict template and the reference facts | The template turns structure from a hope into a checkable contract |
| **evaluate** | 7 deterministic checks + 8 independent LLM-judge checks | The core of the system (section 3) |
| **revise** | Writer gets *only* the failed checks, each with evidence and a fix, plus the list of passing checks to protect | Targeted edits converge faster than rewrites and cause fewer regressions |
| **ship / hold** | Ship if all checks pass. Otherwise, after the retry budget, hold the best draft with a "NOT SHIPPED" banner | Terminates, and fails safe |
| **learn** | Updates failure stats; an LLM distils them (and human feedback) into writer rules for future runs | Self-evolution (section 5) |

**Engine.** The nodes are plain functions over a state dict. With `langgraph` installed they are wired into a `StateGraph` with a conditional edge on `route()`. Without it, a 10-line built-in runner executes the same graph. I chose this because the *graph* is the design and the framework is an implementation detail. It also means reviewers can run it with zero dependencies.

**Model-agnostic.** One `LLM.call(system, user)` interface over Anthropic, OpenAI, Gemini and any OpenAI-compatible API (Groq, OpenRouter, Ollama), using raw HTTP. The **writer and the judge can be different models**, set through env vars. That is the cheapest defence against a model preferring its own writing.

---

## 3. The evaluator

### 3.1 Rubric: 15 hard pass/fail checks

A lesson ships only if **all 15** pass. There is no weighting and no partial credit, because an average hides the one failure that loses a learner.

| ID | Dimension | Check | How |
|---|---|---|---|
| D1 | flow | All 7 sections present, in teaching order (What → Why → How → Example → Key words → Recap → Quiz) | code |
| D2 | coverage | 700–2000 words (one 10–12 minute sitting) | code |
| D3 | language | Average sentence ≤ 16 words, no sentence > 30 | code |
| D4 | language | Flesch Reading Ease ≥ 55 (glossary excluded) | code |
| D5 | language | No words from a hard-vocabulary blocklist (utilize, leverage, paradigm…) | code |
| D6 | jargon | Every jargon term used appears in Key words | code |
| D7 | example | ≥ 3 quiz questions, each with an answer | code |
| J1 | accurate | No claim contradicts the reference facts; no known misconception stated as true | LLM |
| J2 | grounded | Every specific claim (names, dates, numbers, tools) is supported by the facts | LLM |
| J3 | coverage | All 7 key points (a)–(g), including "RAG does not change weights" and "RAG reduces but doesn't remove errors" | LLM |
| J4 | example | One familiar Indian running example, carried through *every* step | LLM |
| J5 | jargon | Every term explained at or before its *first* use | LLM |
| J6 | language | No idioms, slang or Western references; friendly tone | LLM |
| J7 | flow | No forward references, no contradictions, recap matches content | LLM |
| J8 | standalone | Assumes no programming, ML or advanced maths | LLM |

### 3.2 Why split code checks and LLM checks?

**If a property can be measured exactly, measure it in code.** Code checks are free, instant, deterministic and cannot hallucinate. They also give exact, actionable feedback ("this 34-word sentence"). That leaves the LLM judge only the questions that need understanding: truth, coverage, flow and cultural fit.

Some dimensions have **both** a code check and an LLM check on purpose. D6 catches a term missing from the glossary. J5 catches a term *used before it is explained*, which code cannot see.

### 3.3 Making the LLM judge trustworthy

| Risk | Mitigation |
|---|---|
| Vague, holistic grading | **One call per check**, with a check-specific *method* ("list every claim, map each to a fact ID…") |
| Hallucinated verdicts | Must return **evidence quotes** from the lesson; the quote is shown in the log so a human can audit it |
| Leniency | Temperature 0; "If you are unsure, it FAILS". A false fail costs one retry. A false pass ships a bad lesson to a learner. That asymmetry decides it |
| "Accurate" judged from the model's own memory | A curated **reference fact sheet with IDs and a list of known misconceptions** (`knowledge/rag.md`) is the ground truth for both writer and judge. Accuracy becomes "consistent with these facts", which a judge can actually verify |
| Broken JSON or API errors | Robust JSON extraction, one repair retry, then **fail-closed** |
| Self-preference bias | Judge never sees the writer's prompt. Writer and judge can be different models |
| Latency | Judge calls run in parallel threads |

### 3.4 Proving the evaluator works

`--inject-error <mode>` corrupts draft 1 *after* generation and *before* evaluation, which is exactly where a real model mistake would be:

| Mode | What is planted | Expected catch |
|---|---|---|
| `factual` | "RAG works by retraining the model… weights are updated" (misconception M1) | J1 |
| `ungrounded` | "97% accurate… invented by Google in 2015" | J2 |
| `jargon` | One 40-word sentence of unexplained jargon and hard words | D3, D5, J5, J6 |
| `structure` | Deletes the quiz section | D1, D7 |

The test suite asserts each one is caught and that the loop then recovers.

---

## 4. Regeneration strategy

- **Revise, don't restart.** The reviser gets the current draft, *only* the failed checks (reason, evidence quote and a concrete fix), and the list of checks that already pass with an instruction to keep them passing. A full rewrite would throw away the 12 things that were already right.
- **Regression tracking.** If a check that passed in attempt *n* fails in attempt *n+1*, the run log records it as a regression. That is the main risk of any fix loop, so it should be visible.
- **Bounded.** `max_retries` is 2 by default (so at most 3 drafts), and the CLI refuses values above 2. The loop always ends.
- **Fail safe.** When the budget runs out, the system **holds** instead of shipping. It saves the best draft (most checks passed, latest wins ties) with a "NOT SHIPPED – NEEDS HUMAN REVIEW" banner and exits with code 2. A content pipeline should never put a failing lesson in front of a learner just because it ran out of tries.

---

## 5. Memory and self-evolution

`memory/memory.json` persists across runs. It is a plain JSON file, so it is easy to inspect, diff and reset.

| Stored | Used for |
|---|---|
| `failure_counts`, `failure_examples` | Which checks the writer keeps failing, and how |
| `learned_rules` (max 8) | **Prompt evolution.** After a run with real failures, an LLM "refiner" turns the failure history and human feedback into short, specific writer rules. These go into the generator *and* reviser prompts on every future run, so the system prevents a mistake instead of fixing it every time |
| `extra_checks` | **Rubric evolution.** `add-check "…"` lets a reviewer add a new pass/fail check. It is enforced from the next run |
| `human_feedback` | Free-text notes, folded into the next rule refinement |
| `runs` | First-try score per run. `stats` shows whether learning raises the first-try pass rate. That is the metric that matters: fewer retries means lower cost and latency |

Design decisions:
- **Injected errors are not learned from.** A planted demo error is not the writer's fault and would teach the wrong lesson.
- **The rules are capped and rewritten, not appended.** Prompts that grow without limit get worse. The refiner merges and deduplicates.
- **Human feedback goes in at two levels.** "Your writing does X" becomes a writer rule. "Also require Y" becomes a rubric check.

---

## 6. Trade-offs I made

| Choice | Alternative | Why |
|---|---|---|
| 15 binary checks, all must pass | Weighted score with a threshold | The brief asks for no partial credit, and the learner is lost by *any* single failure |
| One judge call per LLM check (8 calls) | One call for the whole rubric | Higher reliability and traceability for about 8× the tokens. Parallel calls keep latency near one call. Cost is still low with a "flash" or "mini"-class judge |
| Curated fact sheet as ground truth | Let the judge use its own knowledge, or live web retrieval | Verifiable, reproducible and auditable. The cost is a one-time ~1-page fact sheet per topic, which an expert should review anyway |
| Strict, fail-closed judge | Lenient judge | Prefer a false reject (one retry) over a false accept (a confused learner) |
| Template with fixed headings | Free-form lesson | Makes structure checkable in code, and gives a consistent learner experience across lessons |
| Stdlib + optional LangGraph | Hard dependency on a framework | Runs anywhere, and the graph logic stays readable |
| JSON-file memory | Vector DB or SQL | Small, auditable state. Easy to swap later |

Rough cost per run: 1 generation + 8 judge calls per attempt + 1 revision per retry + 1 refinement, so 10–29 LLM calls.

## 7. Known limitations and next steps

- **Judge calibration.** Next, I would build a small labelled set of good and bad lessons to measure the judge's precision and recall per check, then tune the prompts or swap the judge model.
- **Readability metrics are English-centric proxies.** A learner-in-the-loop test (comprehension quiz scores from real students) would be the true signal, and could feed `human_feedback` automatically.
- **Learned rules are not yet A/B tested.** A rule should be kept only if the first-try pass rate improves with it.
- **Multilingual output.** The same pipeline could generate a Telugu/Hindi-English glossary or a full translation, with a back-translation check.
- **Per-topic key points.** J3's checklist is RAG-specific. For many topics I would move it into each topic's fact sheet.
