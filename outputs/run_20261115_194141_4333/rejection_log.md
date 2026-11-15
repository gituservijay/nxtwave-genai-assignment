# Rejection log - Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `run_20261115_194141_4333`
- **Final status:** **NEEDS_HUMAN_REVIEW** (attempt 3 of max 3)
- **Generator:** `gemini:gemini-3.6-flash`  |  **Judge:** `openai_compat:openai/gpt-oss-20b`  |  LLM calls: 39

**Rules learned from earlier runs (added to the writer prompt):**

  - [J5_jargon_explained] Explain every technical term in plain language within the main body text at its very first appearance, before using it elsewhere or in Key words.
  - [D6_glossary_coverage] Include every technical term and acronym mentioned in the lesson (e.g., prompt, retrieval, augment, top-k, LLM, chunk) in the Key words glossary.
  - [J2_grounded] Strictly verify proper nouns, acronyms, and factual claims against the reference facts without inventing or altering any details.
  - [J4_teaches_by_example] Feature the running example character explicitly in every single step of the pipeline and mechanism explanation.
  - [D3_sentence_length] Keep sentences under 25 words max and target an average under 14 words by splitting compound sentences.
  - [D1_structure] Include all required sections—Example, Key Words, Lesson Body, Recap, and Quiz—and maintain total word count between 700 and 2000 words.
  - [D7_quiz] Include at least 3 quiz questions at the end, providing an explicit answer for each question.
  - [J3_key_points] Detail the complete process sequence step-by-step (embed, store, retrieve, augment, generate) without skipping any core stage.

## Score per attempt

| Check | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|
| D1_structure | PASS | PASS | PASS |
| D2_length | PASS | PASS | PASS |
| D3_sentence_length | PASS | PASS | PASS |
| D4_readability | PASS | PASS | PASS |
| D5_hard_words | PASS | PASS | PASS |
| D6_glossary_coverage | PASS | PASS | PASS |
| D7_quiz | PASS | PASS | PASS |
| J1_accurate | PASS | PASS | PASS |
| J2_grounded | **FAIL** | **FAIL** | **FAIL** |
| J3_key_points | PASS | PASS | PASS |
| J4_teaches_by_example | PASS | PASS | PASS |
| J5_jargon_explained | **FAIL** | **FAIL** | **FAIL** |
| J6_language_fit | PASS | **FAIL** | PASS |
| J7_flow | **FAIL** | PASS | PASS |
| J8_standalone | PASS | PASS | PASS |
| **Total** | **12/15** | **12/15** | **13/15** |

## Attempt 1 - REJECTED (12/15)

**What failed and why:**

- **J2_grounded** (accurate & grounded, llm check): Judge error (fail-closed): no JSON object found
- **J5_jargon_explained** (clear, no unexplained jargon, llm check): Technical terms 'retrieve', 'generate', and 'hallucinate' are used before being explained in the body.
  - Evidence: _"The system first finds (retrieves) helpful text pieces from a collection of documents."_
  - Fix requested: Add a simple definition for each term immediately after its first use in the body text, e.g., after the first use of 'retrieve', write: 'Retrieve means to search and find relevant pieces of text.' Do the same for 'generate' and 'hallucinate'.
- **J7_flow** (coherent teaching flow, llm check): The lesson references "keyword search" without explaining it, creating a forward reference to an unexplained idea.
  - Evidence: _"Retrieval can also use keyword search, or a mix of keyword and meaning search (hybrid search)."_
  - Fix requested: Add a brief explanation of what keyword search is, e.g., "Keyword search looks for exact words or phrases in the documents, unlike semantic search which uses meaning."

## Attempt 2 - REJECTED (12/15)

**What changed on this retry (feedback sent to the writer):**

```
- [J2_grounded] Judge error (fail-closed): no JSON object found
  Evidence: -
  Fix: -
- [J5_jargon_explained] Technical terms 'retrieve', 'generate', and 'hallucinate' are used before being explained in the body.
  Evidence: "The system first finds (retrieves) helpful text pieces from a collection of documents."
  Fix: Add a simple definition for each term immediately after its first use in the body text, e.g., after the first use of 'retrieve', write: 'Retrieve means to search and find relevant pieces of text.' Do the same for 'generate' and 'hallucinate'.
- [J7_flow] The lesson references "keyword search" without explaining it, creating a forward reference to an unexplained idea.
  Evidence: "Retrieval can also use keyword search, or a mix of keyword and meaning search (hybrid search)."
  Fix: Add a brief explanation of what keyword search is, e.g., "Keyword search looks for exact words or phrases in the documents, unlike semantic search which uses meaning."
```

**Regressions** (passed before, failed now): J6_language_fit

**What failed and why:**

- **J2_grounded** (accurate & grounded, llm check): Judge error (fail-closed): no JSON object found
- **J5_jargon_explained** (clear, no unexplained jargon, llm check): The first use of the term RAG is not immediately explained.
  - Evidence: _"Retrieval-Augmented Generation (RAG) helps computer programs search documents to give correct answers to questions." (RAG appears here before its explanation in the next sentence.)_
  - Fix requested: Explain RAG in the same sentence or immediately before its first use, e.g., "RAG (Retrieval-Augmented Generation) is a technique that…"
- **J6_language_fit** (beginner-friendly language, llm check): Judge error (fail-closed): no JSON object found

## Attempt 3 - REJECTED (13/15)

**What changed on this retry (feedback sent to the writer):**

```
- [J2_grounded] Judge error (fail-closed): no JSON object found
  Evidence: -
  Fix: -
- [J5_jargon_explained] The first use of the term RAG is not immediately explained.
  Evidence: "Retrieval-Augmented Generation (RAG) helps computer programs search documents to give correct answers to questions." (RAG appears here before its explanation in the next sentence.)
  Fix: Explain RAG in the same sentence or immediately before its first use, e.g., "RAG (Retrieval-Augmented Generation) is a technique that…"
- [J6_language_fit] Judge error (fail-closed): no JSON object found
  Evidence: -
  Fix: -
```

**What failed and why:**

- **J2_grounded** (accurate & grounded, llm check): Judge error (fail-closed): no JSON object found
- **J5_jargon_explained** (clear, no unexplained jargon, llm check): Judge error (fail-closed): no JSON object found
