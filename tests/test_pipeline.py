"""Offline tests (mock model): python -m pytest -q"""
from pathlib import Path

import pytest

from lessonforge.checks_code import CODE_CHECKS
from lessonforge.inject import MODES, inject
from lessonforge.llm import LLM, LLMConfig, extract_json
from lessonforge.memory import Memory
from lessonforge.mock import MockResponder, flawed_first_draft
from lessonforge.pipeline import Pipeline

GOOD = (Path(__file__).parent.parent / "lessonforge" / "fixtures" / "good_lesson.md").read_text()


def mock_llm():
    return LLM(LLMConfig("mock", "mock"), MockResponder())


def make(tmp_path, **kw):
    return Pipeline(mock_llm(), mock_llm(), Memory(tmp_path / "mem.json"), tmp_path / "out",
                    log=lambda *_: None, engine="builtin", **kw)


def test_good_lesson_passes_all_code_checks():
    assert all(f(GOOD).passed for f in CODE_CHECKS.values())


def test_flawed_draft_fails_specific_checks():
    failed = {k for k, f in CODE_CHECKS.items() if not f(flawed_first_draft()).passed}
    assert failed == {"D3_sentence_length", "D5_hard_words", "D6_glossary_coverage"}


def test_loop_regenerates_then_ships(tmp_path):
    s = make(tmp_path).run("Introduction to RAG")
    assert s["status"] == "SHIPPED"
    assert len(s["attempts"]) == 2
    assert not s["attempts"][0].evaluation.passed
    out = Path(s["out_dir"])
    assert (out / "lesson.md").exists() and (out / "rejection_log.md").exists()


def test_loop_terminates_and_holds_when_budget_is_zero(tmp_path):
    s = make(tmp_path, max_retries=0).run("RAG")
    assert s["status"] == "NEEDS_HUMAN_REVIEW"
    assert len(s["attempts"]) == 1
    assert "NOT SHIPPED" in (Path(s["out_dir"]) / "lesson.md").read_text()


@pytest.mark.parametrize("mode,expected", [
    ("factual", "J1_accurate"), ("ungrounded", "J2_grounded"),
    ("jargon", "J5_jargon_explained"), ("structure", "D7_quiz"),
])
def test_evaluator_catches_injected_errors(tmp_path, mode, expected):
    s = make(tmp_path, inject_mode=mode).run("RAG")
    first = {r.id for r in s["attempts"][0].evaluation.failed}
    assert expected in first
    assert s["status"] == "SHIPPED"  # and the loop recovers


def test_memory_learns_rules_across_runs(tmp_path):
    make(tmp_path).run("RAG")
    mem = Memory(tmp_path / "mem.json")
    assert mem.data["learned_rules"], "rules should be learned from failures"
    assert mem.data["failure_counts"]["D5_hard_words"] == 1
    p2 = Pipeline(mock_llm(), mock_llm(), mem, tmp_path / "out", log=lambda *_: None, engine="builtin")
    s2 = p2.run("RAG")
    assert s2["rules"], "second run must inject learned rules into the prompt"


def test_human_added_check_is_enforced(tmp_path):
    mem = Memory(tmp_path / "mem.json")
    mem.add_check("Mentions at least one Indian city.")
    mem.save()
    s = make(tmp_path).run("RAG")
    assert any(r.id == "H1_custom" for r in s["attempts"][0].evaluation.results)


def test_judge_fails_closed_on_garbage():
    from lessonforge.evaluator import Evaluator
    junk = LLM(LLMConfig("mock", "mock"), lambda *a: "not json at all")
    ev = Evaluator(junk, "facts").evaluate(GOOD)
    assert all(not r.passed for r in ev.results if r.kind == "llm")


def test_extract_json_handles_fences():
    assert extract_json('Sure!\n```json\n{"passed": true}\n```') == {"passed": True}


def test_all_injection_modes_change_text():
    for m in MODES:
        assert inject(GOOD, m)[0] != GOOD
