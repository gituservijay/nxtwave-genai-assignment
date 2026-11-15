"""The agentic loop:  load memory -> generate -> evaluate -> (revise -> evaluate)* -> decide -> learn

    +-----------+    +----------+    +----------+  pass   +--------+    +-------+
    |  context  |--->| generate |--->| evaluate |-------->|  ship  |--->| learn |
    | (memory)  |    +----------+    +----------+         +--------+    +-------+
    +-----------+                      |    ^   fail &               ^
                                       |    |   retries left          |
                                       v    |                         |
                                     +--------+   fail & no retries   |
                                     | revise |   -> hold for human --+
                                     +--------+

Nodes are plain functions over a state dict. If LangGraph is installed the same nodes are
wired into a StateGraph (see build_langgraph); otherwise a tiny built-in runner executes
the same graph. Both paths produce identical results.
"""
from __future__ import annotations

import json
import re
import shutil
import time
from pathlib import Path
from typing import Any

from .evaluator import Evaluator
from .generator import Generator
from .inject import inject
from .llm import LLM
from .memory import Memory
from .models import Attempt
from .prompts import REFINE_SYSTEM, REFINE_USER

KNOWLEDGE = Path(__file__).parent / "knowledge"

State = dict[str, Any]


def load_facts(topic: str) -> str:
    # One curated reference sheet per topic. "rag" is matched loosely.
    t = topic.lower()
    if "retrieval" in t:
        t += " rag"
    for p in sorted(KNOWLEDGE.glob("*.md")):
        if p.stem.lower() in re.findall(r"[a-z0-9]+", t):
            return p.read_text(encoding="utf-8")
    raise FileNotFoundError(f"No reference facts for topic '{topic}'. Add {KNOWLEDGE}/<topic-keyword>.md")


class Pipeline:
    def __init__(self, gen_llm: LLM, judge_llm: LLM, memory: Memory, out_dir: str | Path = "outputs",
                 max_retries: int = 2, inject_mode: str | None = None, learn: bool = True, log=print,
                 engine: str = "auto"):
        self.engine = engine
        self.gen_llm, self.judge_llm, self.memory = gen_llm, judge_llm, memory
        self.out_root = Path(out_dir)
        self.max_retries = max_retries
        self.inject_mode = inject_mode
        self.learn_enabled = learn
        self.log = log

    # ------------------------------------------------------------------ nodes
    def node_context(self, s: State) -> State:
        s["facts"] = load_facts(s["topic"])
        s["rules"] = self.memory.rules_text()
        s["generator"] = Generator(self.gen_llm, s["facts"])
        s["evaluator"] = Evaluator(self.judge_llm, s["facts"], self.memory.extra_checks())
        s["attempts"] = []
        self.log(f"[context] topic='{s['topic']}' | rubric checks={len(s['evaluator'].rubric)} "
                 f"| learned rules in prompt={len(self.memory.data['learned_rules'])}")
        if s["rules"]:
            self.log("          rules:\n" + "\n".join("            " + l for l in s["rules"].splitlines()))
        return s

    def node_generate(self, s: State) -> State:
        self.log("[generate] writing first draft ...")
        draft = s["generator"].generate(s["topic"], s["rules"])
        injected = None
        if self.inject_mode:
            draft, injected = inject(draft, self.inject_mode)
            self.log(f"[inject]   DELIBERATE ERROR ({self.inject_mode}): {injected}")
        s["draft"], s["pending_changes"], s["pending_injection"] = draft, [], injected
        return s

    def node_evaluate(self, s: State) -> State:
        n = len(s["attempts"]) + 1
        self.log(f"[evaluate] attempt {n}: running {len(s['evaluator'].rubric)} checks ...")
        ev = s["evaluator"].evaluate(s["draft"])
        regressions = []
        if s["attempts"]:
            prev = {r.id: r.passed for r in s["attempts"][-1].evaluation.results}
            regressions = [r.id for r in ev.results if prev.get(r.id) and not r.passed]
        att = Attempt(n, s["draft"], ev, s.get("pending_changes", []), s.get("pending_injection"), regressions)
        s["attempts"].append(att)
        try:  # save progress immediately (survives Ctrl+C / crashes)
            d = self.out_root / s["run_id"] / "drafts"
            d.mkdir(parents=True, exist_ok=True)
            (d / f"attempt_{n}.md").write_text(s["draft"], encoding="utf-8")
            (d / f"attempt_{n}_scores.json").write_text(json.dumps(ev.to_dict(), indent=2, ensure_ascii=False),
                                                        encoding="utf-8")
        except OSError:
            pass
        for r in ev.results:
            self.log(f"           {'PASS' if r.passed else 'FAIL'}  {r.id:<24} {r.reason[:110]}")
        self.log(f"           => {ev.score}/{len(ev.results)} {'SHIP' if ev.passed else 'REJECT'}"
                 + (f" | regressions: {regressions}" if regressions else ""))
        return s

    def route(self, s: State) -> str:
        last = s["attempts"][-1]
        if last.evaluation.passed:
            return "ship"
        if any("daily quota" in r.reason for r in last.evaluation.results):
            self.log("[route]    judge's daily API quota is exhausted -> stop now and hold the best draft "
                     "(switch LF_JUDGE_MODEL or wait for the reset)")
            return "hold"
        if len(s["attempts"]) - 1 < self.max_retries:
            return "revise"
        return "hold"

    def node_revise(self, s: State) -> State:
        last = s["attempts"][-1]
        failed = last.evaluation.failed
        passed = [r for r in last.evaluation.results if r.passed]
        self.log(f"[revise]   fixing {len(failed)} failed check(s): {', '.join(r.id for r in failed)}")
        s["draft"], s["pending_changes"] = s["generator"].revise(s["topic"], s["draft"], failed, passed, s["rules"])
        s["pending_injection"] = None
        return s

    def node_ship(self, s: State) -> State:
        s["status"] = "SHIPPED"
        s["final"] = s["attempts"][-1]
        self.log(f"[ship]     passed all checks on attempt {s['final'].number}")
        return s

    def node_hold(self, s: State) -> State:
        # Retry budget exhausted: never ship a failing lesson silently. Keep the best draft
        # (most checks passed; latest wins ties) and flag it for a human.
        best = max(s["attempts"], key=lambda a: (a.evaluation.score, a.number))
        s["status"], s["final"] = "NEEDS_HUMAN_REVIEW", best
        self.log(f"[hold]     retries exhausted; best draft = attempt {best.number} "
                 f"({best.evaluation.score}/{len(best.evaluation.results)}). Flagged for human review.")
        return s

    def node_learn(self, s: State) -> State:
        # Failures from attempt 1 are the honest signal of what the WRITER gets wrong
        # (an injected error is excluded - it is not the writer's fault).
        for a in s["attempts"]:
            if a.injected_error:
                continue
            # Judge/API errors (e.g. rate limits) say nothing about the writing - don't learn from them.
            self.memory.record_failures([r for r in a.evaluation.failed if not r.reason.startswith("Judge error")])
        first = s["attempts"][0]
        self.memory.record_run({
            "run_id": s["run_id"], "topic": s["topic"], "status": s["status"],
            "shipped": s["status"] == "SHIPPED", "attempts": len(s["attempts"]),
            "first_score": f"{first.evaluation.score}/{len(first.evaluation.results)}",
            "first_failed": [r.id for r in first.evaluation.failed],
            "rules_used": len(self.memory.data["learned_rules"]),
            "injected": self.inject_mode,
        })
        organic_fail = any(r for a in s["attempts"] if not a.injected_error
                           for r in a.evaluation.failed if not r.reason.startswith("Judge error"))
        if self.learn_enabled and (organic_fail or self.memory.data["human_feedback"]):
            self.refine_rules(s["run_id"])
        self.memory.save()
        return s

    # ------------------------------------------------------------------ self-evolution
    def refine_rules(self, run_id: str) -> None:
        try:
            fb = "\n".join(f"- {f['note']}" for f in self.memory.data["human_feedback"][-10:]) or "(none)"
            out = self.gen_llm.call_json(
                REFINE_SYSTEM,
                REFINE_USER.format(history=self.memory.history_text(), feedback=fb,
                                   existing=self.memory.rules_text() or "(none)"),
                tag="refine",
            )
            rules = out.get("rules", [])
            if rules:
                self.memory.set_rules(rules, run_id)
                self.log(f"[learn]    updated {len(rules)} writer rule(s) for future runs")
        except Exception as e:
            self.log(f"[learn]    rule refinement skipped: {e}")

    # ------------------------------------------------------------------ run
    def run(self, topic: str) -> State:
        s: State = {"topic": topic, "run_id": time.strftime("run_%Y%m%d_%H%M%S_") + f"{time.time_ns() % 10**6:06d}"[:4]}
        s = self.execute(s)
        s["out_dir"] = str(self.write_outputs(s))
        return s

    def execute(self, s: State) -> State:
        graph = build_langgraph(self) if self.engine != "builtin" else None
        if graph is not None:
            self.log("[engine]   LangGraph StateGraph")
            return graph.invoke(s, {"recursion_limit": 50})
        self.log("[engine]   built-in runner (pip install langgraph to use LangGraph)")
        s = self.node_context(s)
        s = self.node_generate(s)
        s = self.node_evaluate(s)
        while (nxt := self.route(s)) == "revise":
            s = self.node_revise(s)
            s = self.node_evaluate(s)
        s = self.node_ship(s) if nxt == "ship" else self.node_hold(s)
        return self.node_learn(s)

    # ------------------------------------------------------------------ outputs
    def write_outputs(self, s: State) -> Path:
        from .report import rejection_log_md

        out = self.out_root / s["run_id"]
        (out / "drafts").mkdir(parents=True, exist_ok=True)
        for a in s["attempts"]:
            (out / "drafts" / f"attempt_{a.number}.md").write_text(a.lesson, encoding="utf-8")
        final = s["final"]
        banner = "" if s["status"] == "SHIPPED" else (
            "> **NOT SHIPPED - NEEDS HUMAN REVIEW.** This is the best draft; some checks still fail. "
            "See rejection_log.md.\n\n")
        (out / "lesson.md").write_text(banner + final.lesson, encoding="utf-8")
        log = {
            "run_id": s["run_id"], "topic": s["topic"], "status": s["status"],
            "final_attempt": final.number, "max_retries": self.max_retries,
            "generator_model": f"{self.gen_llm.cfg.provider}:{self.gen_llm.cfg.model}",
            "judge_model": f"{self.judge_llm.cfg.provider}:{self.judge_llm.cfg.model}",
            "llm_calls": self.gen_llm.calls + (self.judge_llm.calls if self.judge_llm is not self.gen_llm else 0),
            "learned_rules_used": s["rules"].splitlines() if s["rules"] else [],
            "attempts": [
                {"attempt": a.number, "injected_error": a.injected_error,
                 "changes_requested": a.changes_requested, "regressions": a.regressions,
                 **a.evaluation.to_dict()} for a in s["attempts"]
            ],
        }
        (out / "rejection_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
        (out / "rejection_log.md").write_text(rejection_log_md(log), encoding="utf-8")
        latest = self.out_root / "latest"
        if latest.exists():
            shutil.rmtree(latest)
        shutil.copytree(out, latest)
        self.log(f"[output]   {out}/lesson.md  +  rejection_log.md  (copied to {latest})")
        return out


def build_langgraph(p: Pipeline):
    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        return None
    from typing import TypedDict

    class LGState(TypedDict, total=False):  # every key is a plain "last value wins" channel
        topic: str
        run_id: str
        facts: str
        rules: str
        generator: Any
        evaluator: Any
        attempts: list
        draft: str
        pending_changes: list
        pending_injection: Any
        status: str
        final: Any

    g = StateGraph(LGState)
    for name in ("context", "generate", "evaluate", "revise", "ship", "hold", "learn"):
        g.add_node(name, getattr(p, f"node_{name}"))
    g.set_entry_point("context")
    g.add_edge("context", "generate")
    g.add_edge("generate", "evaluate")
    g.add_conditional_edges("evaluate", p.route, {"ship": "ship", "revise": "revise", "hold": "hold"})
    g.add_edge("revise", "evaluate")
    g.add_edge("ship", "learn")
    g.add_edge("hold", "learn")
    g.add_edge("learn", END)
    return g.compile()
