"""OFFLINE TEST DOUBLE - not a real model.

Lets anyone (and the test suite) run the whole loop with no API key:
  * generate -> a canned first draft with realistic flaws (long sentence, hard word,
    missing glossary entry), so the evaluator has something real to reject;
  * revise   -> the canned clean lesson;
  * judge    -> simple keyword heuristics that catch the injected demo errors;
  * refine   -> rules derived from the failure history.
Real runs use a real LLM for every one of these steps.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

FIX = Path(__file__).parent / "fixtures"


def flawed_first_draft() -> str:
    good = (FIX / "good_lesson.md").read_text()
    bad = good.replace(
        "An LLM is a computer program that has read a huge amount of text.",
        "An LLM is a computer program that has been trained on an extremely large collection of text from books, "
        "websites and many other places, which is why it can utilize patterns in language to answer questions.",
    )
    bad = re.sub(r"(?m)^- \*\*Context window\*\*.*\n", "", bad)
    return bad


class MockResponder:
    def __call__(self, system: str, user: str, tag: str) -> str:
        if tag == "generate":
            return flawed_first_draft()
        if tag == "revise":
            return (FIX / "good_lesson.md").read_text()
        if tag == "refine":
            ids = re.findall(r"^(\w+_\w+): failed", user, re.M)
            rules = [{"check_id": i, "rule": f"Pre-empt {i}: re-read the draft for this before finishing."} for i in ids[:8]]
            return json.dumps({"rules": rules})
        if tag.startswith("judge:"):
            return json.dumps(self.judge(tag.split(":", 1)[1], user))
        raise ValueError(tag)

    @staticmethod
    def judge(cid: str, user: str) -> dict:
        lesson = user.split("<<<", 1)[-1].rsplit(">>>", 1)[0]
        low = lesson.lower()
        bad = {
            "J1_accurate": r"rag works by retraining[^.]*|weights are updated[^.]*",
            "J2_grounded": r"[^.]*\d+% accurate[^.]*|invented by google[^.]*",
            "J5_jargon_explained": r"[^.]*cosine similarity[^.]*",
            "J6_language_fit": r"[^.]*\bleverages\b[^.]*",
        }.get(cid)
        m = re.search(bad, low) if bad else None
        if m:
            return {"passed": False, "reason": f"[mock judge] problem found for {cid}.",
                    "evidence": m.group(0).strip()[:200], "fix": "Remove or correct the quoted text."}
        return {"passed": True, "reason": f"[mock judge] no problem found for {cid}.", "evidence": "-", "fix": ""}
