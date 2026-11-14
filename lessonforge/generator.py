from __future__ import annotations

import re

from .llm import LLM
from .models import CheckResult
from .prompts import GEN_SYSTEM, GEN_USER, PITFALLS_BLOCK, REVISE_SYSTEM, REVISE_USER


def clean(md: str) -> str:
    """Strip code fences / chatter some models wrap around the lesson."""
    md = md.strip()
    m = re.match(r"^```(?:markdown|md)?\s*\n(.*)\n```\s*$", md, re.S)
    if m:
        md = m.group(1)
    i = md.find("# ")
    return md[i:].strip() + "\n" if i > 0 else md + "\n"


class Generator:
    def __init__(self, llm: LLM, facts: str):
        self.llm = llm
        self.facts = facts

    def generate(self, topic: str, learned_rules: str = "") -> str:
        pitfalls = PITFALLS_BLOCK.format(rules=learned_rules) if learned_rules else ""
        out = self.llm.call(GEN_SYSTEM, GEN_USER.format(topic=topic, facts=self.facts, pitfalls=pitfalls), tag="generate")
        return clean(out)

    def revise(self, topic: str, draft: str, failed: list[CheckResult], passed: list[CheckResult],
               learned_rules: str = "") -> tuple[str, list[str]]:
        feedback = [
            f"- [{r.id}] {r.reason}\n  Evidence: {r.evidence or '-'}\n  Fix: {r.fix or '-'}" for r in failed
        ]
        system = REVISE_SYSTEM + (PITFALLS_BLOCK.format(rules=learned_rules) if learned_rules else "")
        out = self.llm.call(
            system,
            REVISE_USER.format(topic=topic, facts=self.facts, feedback="\n".join(feedback),
                               passing=", ".join(r.id for r in passed) or "(none)", draft=draft),
            tag="revise",
        )
        return clean(out), feedback
