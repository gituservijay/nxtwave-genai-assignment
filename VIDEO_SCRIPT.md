# Loom video plan (target: 17 minutes)

Keep your camera bubble on the whole time. Have these tabs ready before you start: the terminal (font size 16+), the repo in VS Code, the README (with the rendered Mermaid diagram), DESIGN.md, and `outputs/latest/rejection_log.md`.

Before recording: run `python -m lessonforge reset-memory`. Do one practice run so you know how long a real run takes.

---

### 0:00–1:30: Intro and problem framing (camera-focused)
- Your name, and the one-line goal: "a system that decides on its own whether a lesson is good enough to ship".
- Who the learner is, and why that changes everything: for a reader with limited English, readability is correctness, not style.
- The four questions you designed around (DESIGN.md §1).

### 1:30–4:30: Architecture walkthrough
- Show the Mermaid diagram in the README. Walk through the nodes: context → generate → evaluate → revise/ship/hold → learn → memory.
- Open `pipeline.py`. Point at `route()`, the retry budget, and `node_hold` ("never ship a failing lesson silently").
- Mention: same nodes run on LangGraph or the built-in runner; writer and judge can be different models.

### 4:30–8:00: The evaluator (the most important part)
- Open `rubric.json`: 15 binary checks, all must pass, no partial credit.
- Explain why code checks come first (`checks_code.py`: sentence length, readability, hard words, glossary, quiz). They are free, deterministic and can't hallucinate.
- Open `prompts.py` → `JUDGE_SYSTEM` and `JUDGE_HINTS`. Cover one call per check, evidence quotes required, "if unsure, FAIL", temperature 0, and fail-closed on errors.
- Open `knowledge/rag.md`. The fact sheet with IDs and misconceptions is the ground truth, which makes "accurate" checkable.

### 8:00–11:00: Live end-to-end run
```bash
python -m lessonforge run
```
- Narrate as it prints: first draft → the 15 PASS/FAIL lines → revise with the specific failed checks → re-evaluate → SHIP.
- Open `outputs/latest/rejection_log.md`: the per-attempt scorecard, evidence quotes, and "what changed on this retry".
- Open `outputs/latest/lesson.md`. Scroll it: open-book exam analogy, running example in every step, Key words, quiz.

### 11:00–14:00: Evaluator catching a deliberate error
```bash
python -m lessonforge run --inject-error factual
```
- Show the `[inject]` line with the planted misconception ("RAG retrains the model…").
- Show `J1_accurate` FAIL with the **quoted evidence**. Then show the revision removing it and the final SHIP.
- Optionally run `--inject-error jargon` too: several checks fail at once (D3, D5, J5, J6).
- Show the failsafe: `python -m lessonforge run --max-retries 0` → NEEDS_HUMAN_REVIEW, exit code 2, banner in lesson.md.

### 14:00–16:00: Memory and self-evolution
```bash
python -m lessonforge stats
python -m lessonforge feedback "Use more examples from Indian college life"
python -m lessonforge add-check "Every step of 'How does RAG work?' ends with an example line"
python -m lessonforge run
```
- Show the learned rules being loaded into the prompt in the `[context]` line, and the new H1 check being enforced.
- Explain why injected errors are not learned from, and why rules are capped and rewritten.

### 16:00–17:30: Trade-offs, limits, close (camera-focused)
- 2–3 trade-offs from DESIGN.md §6: binary vs weighted, per-check judge calls vs one call, strict vs lenient.
- What you'd do next: judge calibration set, real learner comprehension data, multilingual glossary.
- Thank them.

**Tip:** if a live API call is slow, keep talking over it about the design. Don't cut the run.
