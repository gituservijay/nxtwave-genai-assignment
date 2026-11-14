"""Deliberate-error injection for the demo: proves the evaluator catches real problems.

The error is injected into the FIRST draft only, after generation and before evaluation.
That is exactly where a real model mistake would sit, so the rest of the loop (evaluate ->
feedback -> revise) runs exactly as it would in production.
"""
from __future__ import annotations

import re

INJECTIONS = {
    # Classic misconception M1 - a factual error the judge must catch (J1_accurate).
    "factual": (
        "what",
        "RAG works by retraining the AI model on your documents, so the model permanently "
        "learns them and its weights are updated every time you add a file.",
    ),
    # Jargon used before it is explained + hard vocabulary + one very long sentence
    # (J5_jargon_explained, D3_sentence_length, D5_hard_words, J6_language_fit).
    "jargon": (
        "what",
        "Essentially, RAG leverages dense vector embeddings and cosine similarity over a "
        "high-dimensional latent space to facilitate semantic retrieval of top-k chunks, "
        "which are subsequently concatenated into the context window of the transformer-based "
        "LLM for conditional generation.",
    ),
    # Made-up specific fact not in the reference sheet (J2_grounded).
    "ungrounded": (
        "why",
        "Studies show RAG makes answers 97% accurate, and it was invented by Google in 2015.",
    ),
}

MODES = sorted(list(INJECTIONS) + ["structure"])


def inject(lesson: str, mode: str) -> tuple[str, str]:
    """Return (corrupted_lesson, description)."""
    if mode == "structure":
        out = re.sub(r"(?ms)^##\s*check your understanding.*", "", lesson, flags=re.I | re.M | re.S)
        return out.rstrip() + "\n", "Removed the whole 'Check your understanding' section"
    if mode not in INJECTIONS:
        raise ValueError(f"unknown injection mode {mode}; choose from {MODES}")
    section, sentence = INJECTIONS[mode]
    pat = {"what": r"(?im)^##\s*what\b.*$", "why": r"(?im)^##\s*why\b.*$"}[section]
    m = re.search(pat, lesson)
    if not m:  # no such heading: put it right after the title
        m = re.search(r"(?m)^#\s.*$", lesson)
    pos = m.end() if m else 0
    out = lesson[:pos] + "\n\n" + sentence + "\n" + lesson[pos:]
    return out, f"Inserted into '{section}' section: \"{sentence}\""
