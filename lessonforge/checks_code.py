"""Deterministic (code-based) rubric checks.

Rule of thumb used in this project: if a property can be measured exactly, measure it in
code. Code checks are free, instant, never hallucinate, and give the same answer every
time - which makes the LLM judge's job smaller and the whole evaluator more trustworthy.
"""
from __future__ import annotations

import re

from .models import CheckResult

# H2 headings the generator is told to use, in this order. Regexes are loose on purpose
# (the model may write "What is RAG?" or "What Is Retrieval-Augmented Generation").
REQUIRED_SECTIONS = [
    ("what", r"^what\b"),
    ("why", r"^why\b"),
    ("how", r"^how\b.*\bwork"),
    ("example", r"example"),
    ("keywords", r"key\s*words|glossary"),
    ("recap", r"recap|summary"),
    ("quiz", r"check your understanding|quiz"),
]

HARD_WORDS = [
    "utilize", "utilise", "leverage", "paradigm", "facilitate", "plethora", "myriad", "aforementioned",
    "henceforth", "notwithstanding", "consequently", "subsequently", "furthermore", "moreover",
    "ubiquitous", "robust", "seamless", "seamlessly", "holistic", "synergy", "paramount", "elucidate",
    "comprehend", "endeavor", "endeavour", "commence", "pivotal", "intricate", "nuanced", "delve",
    "realm", "tapestry", "whilst", "thereby", "wherein", "albeit",
]

# term -> variants that count as "using" it. A term is only required in the glossary if used.
JARGON = {
    "LLM / large language model": [r"\bllms?\b", r"large language models?"],
    "embedding": [r"\bembeddings?\b"],
    "vector database": [r"vector (database|store|db)s?"],
    "chunk": [r"\bchunks?\b", r"\bchunking\b"],
    "prompt": [r"\bprompts?\b"],
    "retrieval": [r"\bretriev(al|e|es|ed|ing)\b"],
    "hallucination": [r"\bhallucinat(e|es|ed|ion|ions|ing)\b"],
    "context window": [r"context window"],
    "fine-tuning": [r"fine[- ]?tun(e|ing|ed)"],
    "top-k": [r"\btop[- ]?k\b"],
    "augment": [r"\baugment(s|ed|ing|ation)?\b"],
}


def split_sections(md: str) -> list[tuple[str, str]]:
    """Return [(heading_text, body)] for H2 sections."""
    parts = re.split(r"(?m)^##\s+(.+?)\s*$", md)
    out = []
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1] if i + 1 < len(parts) else ""))
    return out


def find_section(md: str, key: str) -> str:
    pat = dict(REQUIRED_SECTIONS)[key]
    for h, body in split_sections(md):
        if re.search(pat, h.lower().strip(" #*?:0-9.")):
            return body
    return ""


def plain_text(md: str) -> str:
    t = re.sub(r"```.*?```", " ", md, flags=re.S)
    t = re.sub(r"(?m)^#+\s.*$", " ", t)              # headings are not sentences
    t = re.sub(r"(?m)^\s*\|.*\|\s*$", " ", t)        # tables
    t = re.sub(r"<[^>]+>", " ", t)                   # html tags (e.g. <details>)
    t = re.sub(r"[*_`>#]", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t


def sentences(md: str) -> list[str]:
    t = plain_text(md)
    sents = []
    for line in t.splitlines():
        line = re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", line).strip()  # bullets/numbered items
        if not line:
            continue
        for s in re.split(r"(?<=[.!?])\s+|(?<=[.!?][\"'”’)])\s+", line):
            if len(words(s)) >= 1:
                sents.append(s.strip())
    return sents


def words(s: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", s)


def syllables(word: str) -> int:
    w = word.lower().strip("'")
    if not w:
        return 0
    if w.isdigit():
        return max(1, len(w) // 2)
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def flesch(md: str) -> float:
    sents = sentences(md)
    ws = [w for s in sents for w in words(s)]
    if not sents or not ws:
        return 0.0
    syl = sum(syllables(w) for w in ws)
    return 206.835 - 1.015 * (len(ws) / len(sents)) - 84.6 * (syl / len(ws))


def body_without(md: str, *keys: str) -> str:
    out = md
    for k in keys:
        sec = find_section(md, k)
        if sec:
            out = out.replace(sec, "\n")
    return out


# ---------------------------------------------------------------- checks

def check_structure(md: str) -> CheckResult:
    heads = [h.lower().strip(" #*?:0-9.") for h, _ in split_sections(md)]
    positions, missing = [], []
    for key, pat in REQUIRED_SECTIONS:
        idx = next((i for i, h in enumerate(heads) if re.search(pat, h)), None)
        if idx is None:
            missing.append(key)
        else:
            positions.append(idx)
    if missing:
        return CheckResult("D1_structure", False, f"Missing sections: {', '.join(missing)}",
                           evidence=f"Found H2 headings: {heads}",
                           fix="Use exactly these H2 sections in order: What is RAG? / Why does RAG matter? / How does RAG work? / Worked example / Key words / Recap / Check your understanding.")
    if positions != sorted(positions):
        return CheckResult("D1_structure", False, "Sections are out of teaching order",
                           evidence=f"Order found: {heads}",
                           fix="Reorder sections: What -> Why -> How -> Example -> Key words -> Recap -> Check your understanding.")
    return CheckResult("D1_structure", True, "All 7 sections present and in order")


def check_length(md: str) -> CheckResult:
    n = len(words(plain_text(md)))
    ok = 700 <= n <= 2000
    return CheckResult("D2_length", ok, f"{n} words (allowed 700-2000)",
                       fix="" if ok else ("Add more explanation and examples." if n < 700 else "Cut repetition; keep only what a beginner needs."))


def check_sentence_length(md: str) -> CheckResult:
    sents = [s for s in sentences(body_without(md, "keywords")) if len(words(s)) > 0]
    if not sents:
        return CheckResult("D3_sentence_length", False, "No sentences found")
    lens = [len(words(s)) for s in sents]
    avg = sum(lens) / len(lens)
    long_ = [s for s in sents if len(words(s)) > 30]
    ok = avg <= 16 and not long_
    reason = f"Average {avg:.1f} words/sentence (max 16); {len(long_)} sentence(s) over 30 words"
    return CheckResult("D3_sentence_length", ok, reason,
                       evidence=" | ".join(long_[:3]),
                       fix="" if ok else "Split every long sentence into two or three short ones. One idea per sentence.")


def check_readability(md: str) -> CheckResult:
    score = flesch(body_without(md, "keywords"))
    ok = score >= 55
    return CheckResult("D4_readability", ok, f"Flesch Reading Ease {score:.1f} (need >= 55)",
                       fix="" if ok else "Use shorter, more common words and shorter sentences.")


def check_hard_words(md: str) -> CheckResult:
    low = md.lower()
    found = sorted({w for w in HARD_WORDS if re.search(rf"\b{w}\b", low)})
    return CheckResult("D5_hard_words", not found,
                       "No hard words" if not found else f"Hard words found: {', '.join(found)}",
                       fix="" if not found else f"Replace with simple words: {', '.join(found)}.")


def check_glossary(md: str) -> CheckResult:
    gloss = find_section(md, "keywords").lower()
    body = body_without(md, "keywords").lower()
    missing = []
    for term, pats in JARGON.items():
        used = any(re.search(p, body) for p in pats)
        if used and not any(re.search(p, gloss) for p in pats):
            missing.append(term)
    ok = bool(gloss) and not missing
    return CheckResult("D6_glossary_coverage", ok,
                       "Every jargon term used is in Key words" if ok else f"Used but not in Key words: {', '.join(missing) or '(no Key words section)'}",
                       fix="" if ok else f"Add simple one-line meanings for: {', '.join(missing)} in the Key words section.")


def check_quiz(md: str) -> CheckResult:
    quiz = find_section(md, "quiz")
    qs = len(re.findall(r"\?", re.sub(r"(?im)^\s*[*_]*answer\b.*$", "", quiz)))
    ans = len(re.findall(r"(?im)^\s*[*_]*answer\b[*_]*\s*:", quiz))
    ok = qs >= 3 and ans >= qs
    return CheckResult("D7_quiz", ok, f"{qs} question(s), {ans} answer(s) (need >= 3, each answered)",
                       fix="" if ok else "Add at least 3 short questions, each followed by a line starting with 'Answer:'.")


CODE_CHECKS = {
    "D1_structure": check_structure,
    "D2_length": check_length,
    "D3_sentence_length": check_sentence_length,
    "D4_readability": check_readability,
    "D5_hard_words": check_hard_words,
    "D6_glossary_coverage": check_glossary,
    "D7_quiz": check_quiz,
}
