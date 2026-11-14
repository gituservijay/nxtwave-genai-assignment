"""Persistent memory across runs (a plain JSON file - easy to inspect, diff and reset).

What is remembered and why:
  failure_counts / failure_examples  -> which checks keep failing, and how (signal for self-evolution)
  learned_rules                      -> writer instructions distilled from failures; injected into the
                                        generator prompt on every future run (prompt evolution)
  extra_checks                       -> rubric checks added from human feedback (rubric evolution)
  human_feedback                     -> free-text notes from a reviewer
  runs                               -> per-run summary, used to show whether first-try pass rate improves
"""
from __future__ import annotations

import json
import time
from pathlib import Path

DEFAULT = {
    "version": 1,
    "runs": [],
    "failure_counts": {},
    "failure_examples": {},
    "learned_rules": [],
    "extra_checks": [],
    "human_feedback": [],
}


class Memory:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.data = json.loads(json.dumps(DEFAULT))
        if self.path.exists():
            self.data.update(json.loads(self.path.read_text()))

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False))

    # ---- reading
    def rules_text(self) -> str:
        return "\n".join(f"- [{r['check_id']}] {r['rule']}" for r in self.data["learned_rules"])

    def extra_checks(self) -> list[dict]:
        return self.data["extra_checks"]

    # ---- writing
    def record_failures(self, failed) -> None:
        for r in failed:
            self.data["failure_counts"][r.id] = self.data["failure_counts"].get(r.id, 0) + 1
            ex = self.data["failure_examples"].setdefault(r.id, [])
            ex.append(r.reason[:300])
            del ex[:-5]  # keep last 5 examples per check

    def record_run(self, summary: dict) -> None:
        summary["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.data["runs"].append(summary)

    def add_feedback(self, note: str) -> None:
        self.data["human_feedback"].append({"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "note": note})

    def add_check(self, description: str, dimension: str = "human feedback") -> str:
        cid = f"H{len(self.data['extra_checks']) + 1}_custom"
        self.data["extra_checks"].append({"id": cid, "dimension": dimension, "type": "llm", "description": description})
        return cid

    def set_rules(self, rules: list[dict], run_id: str) -> None:
        self.data["learned_rules"] = [
            {"check_id": r.get("check_id", "?"), "rule": r["rule"].strip(), "added_run": run_id}
            for r in rules if r.get("rule")
        ][:8]

    def history_text(self) -> str:
        lines = []
        for cid, n in sorted(self.data["failure_counts"].items(), key=lambda kv: -kv[1]):
            exs = "; ".join(self.data["failure_examples"].get(cid, [])[-3:])
            lines.append(f"{cid}: failed {n}x. e.g. {exs}")
        return "\n".join(lines) or "(none)"

    def stats(self) -> str:
        runs = self.data["runs"]
        if not runs:
            return "No runs yet."
        out = ["run | when | first-try score | attempts | status | rules in prompt | injected error"]
        for r in runs:
            out.append(f"{r['run_id']} | {r['ts']} | {r['first_score']} | {r['attempts']} | {r.get('status')} | {r['rules_used']} | {r.get('injected') or '-'}")
        return "\n".join(out)
