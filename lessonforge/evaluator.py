"""Evaluator = deterministic code checks + one LLM-judge call per semantic check.

Design choices:
  * One judge call PER CHECK (not one call for the whole rubric). A single focused question
    gives more reliable verdicts, and failures are independent and easy to trace.
  * Judge must quote evidence. A verdict with no quote is not trusted.
  * Temperature 0 and "if unsure, FAIL" -> the gate is conservative. A false fail costs one
    retry; a false pass ships a bad lesson to a learner.
  * Fail-closed: if the judge errors or returns junk, the check FAILS.
  * The judge never sees the generator's prompt, only the lesson + reference facts.
  * Judge calls run in parallel (LF_JUDGE_WORKERS threads, default 2; use 1 on strict free-tier rate limits).
  * Only the checks that need ground truth (accuracy, grounding, coverage) receive the reference
    facts. The others judge language/teaching quality from the lesson alone -> ~40% fewer tokens,
    which matters on free tiers with tokens-per-minute/day limits.
  * An infrastructure error (rate limit, empty/garbled reply) is retried once before failing closed,
    so a flaky API is not mistaken for a bad lesson.
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .checks_code import CODE_CHECKS
from .llm import LLM
from .models import CheckResult, Evaluation
from .prompts import JUDGE_HINTS, JUDGE_SYSTEM, JUDGE_USER

RUBRIC_PATH = Path(__file__).parent / "rubric.json"


def load_rubric(extra_checks: list[dict] | None = None) -> list[dict]:
    checks = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))["checks"]
    return checks + list(extra_checks or [])


FACT_CHECKS = {"J1_accurate", "J2_grounded", "J3_key_points"}


class Evaluator:
    def __init__(self, judge: LLM, facts: str, extra_checks: list[dict] | None = None):
        self.judge = judge
        self.facts = facts
        self.rubric = load_rubric(extra_checks)

    def _judge_one(self, check: dict, lesson: str) -> CheckResult:
        desc = check["description"]
        hint = JUDGE_HINTS.get(check["id"])
        if hint:
            desc += "\n" + hint
        facts = self.facts if check["id"] in FACT_CHECKS else "(not needed for this check - judge the lesson itself)"
        last_err, v = None, None
        for _ in range(2):  # one retry on infrastructure errors
            try:
                v = self.judge.call_json(
                    JUDGE_SYSTEM,
                    JUDGE_USER.format(check_id=check["id"], description=desc, facts=facts, lesson=lesson),
                    tag=f"judge:{check['id']}",
                )
                break
            except Exception as e:
                last_err = e
                if "daily quota" in str(e):
                    break  # retrying cannot help
        else:
            v = None
        if v is None or (last_err is not None and "daily quota" in str(last_err)):
            return CheckResult(check["id"], False, f"Judge error (fail-closed): {last_err}", kind="llm",
                               dimension=check.get("dimension", ""))
        try:
            passed = v.get("passed") is True
            evidence = str(v.get("evidence", "")).strip()
            reason = str(v.get("reason", "")).strip()
            if passed is False and not str(v.get("fix", "")).strip():
                v["fix"] = "Fix the problem quoted in the evidence."
            return CheckResult(check["id"], passed, reason, evidence, str(v.get("fix", "")).strip(),
                               check.get("dimension", ""), "llm")
        except Exception as e:  # fail closed
            return CheckResult(check["id"], False, f"Judge error (fail-closed): {e}", kind="llm",
                               dimension=check.get("dimension", ""))

    def evaluate(self, lesson: str) -> Evaluation:
        results: dict[str, CheckResult] = {}
        llm_checks = []
        for c in self.rubric:
            if c["type"] == "code":
                r = CODE_CHECKS[c["id"]](lesson)
                r.dimension = c.get("dimension", "")
                results[c["id"]] = r
            else:
                llm_checks.append(c)
        with ThreadPoolExecutor(max_workers=int(os.getenv("LF_JUDGE_WORKERS", "2"))) as pool:
            for r in pool.map(lambda c: self._judge_one(c, lesson), llm_checks):
                results[r.id] = r
        return Evaluation([results[c["id"]] for c in self.rubric])
