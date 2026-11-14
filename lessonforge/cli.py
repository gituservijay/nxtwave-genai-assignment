"""Command line entry point.

  python -m lessonforge run [--topic "..."] [--inject-error factual|jargon|ungrounded|structure]
                            [--max-retries 2] [--no-learn] [--engine auto|builtin]
  python -m lessonforge eval path/to/lesson.md        # judge any lesson file with the rubric
  python -m lessonforge feedback "note"               # human feedback -> memory -> next run's rules
  python -m lessonforge add-check "description"       # human adds a new pass/fail rubric check
  python -m lessonforge stats                         # first-try score per run (is it learning?)
  python -m lessonforge reset-memory
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .evaluator import Evaluator
from .inject import MODES
from .llm import build_llm
from .memory import Memory
from .pipeline import Pipeline, load_facts

ROOT = Path.cwd()


def _load_dotenv() -> None:
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _llms():
    mock = None
    if (os.getenv("LF_GEN_PROVIDER") == "mock") or not any(
        os.getenv(k) for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_COMPAT_API_KEY")):
        from .mock import MockResponder
        mock = MockResponder()
    gen, judge = build_llm("gen", mock), build_llm("judge", mock)
    if gen.cfg.provider == "mock":
        print("!! No API key found -> using the OFFLINE MOCK model (canned drafts, heuristic judge). "
              "Set a key in .env for a real run.\n")
    return gen, judge


def main(argv=None) -> int:
    _load_dotenv()
    ap = argparse.ArgumentParser(prog="lessonforge", description="Self-evaluating lesson generator")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--topic", default="Introduction to RAG (Retrieval-Augmented Generation)")
    r.add_argument("--inject-error", choices=MODES, default=None)
    r.add_argument("--max-retries", type=int, default=2)
    r.add_argument("--no-learn", action="store_true")
    r.add_argument("--engine", choices=["auto", "builtin"], default="auto")
    r.add_argument("--out", default="outputs")
    r.add_argument("--memory", default="memory/memory.json")
    e = sub.add_parser("eval")
    e.add_argument("path")
    e.add_argument("--topic", default="RAG")
    f = sub.add_parser("feedback")
    f.add_argument("note")
    c = sub.add_parser("add-check")
    c.add_argument("description")
    sub.add_parser("stats")
    sub.add_parser("reset-memory")
    a = ap.parse_args(argv)

    mem_path = getattr(a, "memory", "memory/memory.json")
    mem = Memory(mem_path)

    if a.cmd == "run":
        if not 0 <= a.max_retries <= 2:
            ap.error("--max-retries must be 0, 1 or 2 (the loop must terminate)")
        gen, judge = _llms()
        p = Pipeline(gen, judge, mem, a.out, a.max_retries, a.inject_error, not a.no_learn, engine=a.engine)
        s = p.run(a.topic)
        print(f"\nSTATUS: {s['status']}  |  lesson: {s['out_dir']}/lesson.md")
        return 0 if s["status"] == "SHIPPED" else 2
    if a.cmd == "eval":
        _, judge = _llms()
        ev = Evaluator(judge, load_facts(a.topic), mem.extra_checks()).evaluate(Path(a.path).read_text())
        for res in ev.results:
            print(f"{'PASS' if res.passed else 'FAIL'}  {res.id:<24} {res.reason}")
            if not res.passed and res.evidence:
                print(f"      evidence: {res.evidence[:200]}")
        print(f"=> {ev.score}/{len(ev.results)} {'SHIP' if ev.passed else 'REJECT'}")
        return 0 if ev.passed else 2
    if a.cmd == "feedback":
        mem.add_feedback(a.note)
        mem.save()
        print("Saved. It will be turned into writer rules at the end of the next run.")
    elif a.cmd == "add-check":
        cid = mem.add_check(a.description)
        mem.save()
        print(f"Added rubric check {cid}. It is enforced from the next run.")
    elif a.cmd == "stats":
        print(mem.stats())
        print("\nLearned rules:\n" + (mem.rules_text() or "(none)"))
    elif a.cmd == "reset-memory":
        Path(mem_path).unlink(missing_ok=True)
        print("Memory cleared.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
