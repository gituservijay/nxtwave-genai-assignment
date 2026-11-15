# Rejection log - Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `run_20261115_203624_6999`
- **Final status:** **NEEDS_HUMAN_REVIEW** (attempt 1 of max 3)
- **Generator:** `gemini:gemini-3.6-flash`  |  **Judge:** `openai_compat:openai/gpt-oss-20b`  |  LLM calls: 9

**Rules learned from earlier runs (added to the writer prompt):**

  - [J5_jargon_explained] Define every technical term or acronym (e.g., RAG, weights, retrieve, hallucinate) in plain language at its exact first appearance in the body.
  - [D6_glossary_coverage] List every technical term, acronym, or process word (e.g., prompt, chunk, top-k, augment) mentioned anywhere in the lesson inside the Key Words glossary.
  - [J2_grounded] Strictly use facts, proper nouns, and acronyms provided in the reference data; do not alter names (e.g., FAISS) or introduce unverified claims.
  - [J4_teaches_by_example] Mention the running example character by name in every single step of the pipeline, showing how their specific query/data moves through that step.
  - [D3_sentence_length] Keep all sentences under 25 words and target an average under 14 words by splitting compound clauses into direct statements.
  - [J7_flow] Avoid referencing unexplained terms beforehand, and conclude with a recap section that summarizes all core steps and ideas taught.
  - [D1_structure] Include all required sections (Example, Key Words, Body, Recap, Quiz) and ensure the lesson total is strictly between 700 and 2000 words.
  - [D7_quiz] End the lesson with at least three numbered quiz questions, providing an explicit answer for every question.

## Score per attempt

| Check | Attempt 1 |
|---|---|
| D1_structure | PASS |
| D2_length | PASS |
| D3_sentence_length | PASS |
| D4_readability | PASS |
| D5_hard_words | PASS |
| D6_glossary_coverage | PASS |
| D7_quiz | PASS |
| J1_accurate | **FAIL** |
| J2_grounded | **FAIL** |
| J3_key_points | **FAIL** |
| J4_teaches_by_example | PASS |
| J5_jargon_explained | **FAIL** |
| J6_language_fit | **FAIL** |
| J7_flow | **FAIL** |
| J8_standalone | **FAIL** |
| **Total** | **8/15** |

## Attempt 1 - REJECTED (8/15)

**What failed and why:**

- **J1_accurate** (accurate & grounded, llm check): Judge error (fail-closed): daily quota exhausted for this model: {"error":{"message":"Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01m7d2wdmge58sqmf4ewp78bb8` service tier `on_demand` on tokens per day (TPD): Limit 200000, Used 196867, Req
- **J2_grounded** (accurate & grounded, llm check): Judge error (fail-closed): daily quota exhausted for this model: {"error":{"message":"Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01m7d2wdmge58sqmf4ewp78bb8` service tier `on_demand` on tokens per day (TPD): Limit 200000, Used 196867, Req
- **J3_key_points** (covers the key points, llm check): Judge error (fail-closed): daily quota exhausted for this model: {"error":{"message":"Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01m7d2wdmge58sqmf4ewp78bb8` service tier `on_demand` on tokens per day (TPD): Limit 200000, Used 196864, Req
- **J5_jargon_explained** (clear, no unexplained jargon, llm check): Judge error (fail-closed): daily quota exhausted for this model: {"error":{"message":"Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01m7d2wdmge58sqmf4ewp78bb8` service tier `on_demand` on tokens per day (TPD): Limit 200000, Used 199321, Req
- **J6_language_fit** (beginner-friendly language, llm check): Judge error (fail-closed): daily quota exhausted for this model: {"error":{"message":"Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01m7d2wdmge58sqmf4ewp78bb8` service tier `on_demand` on tokens per day (TPD): Limit 200000, Used 199320, Req
- **J7_flow** (coherent teaching flow, llm check): Judge error (fail-closed): daily quota exhausted for this model: {"error":{"message":"Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01m7d2wdmge58sqmf4ewp78bb8` service tier `on_demand` on tokens per day (TPD): Limit 200000, Used 199320, Req
- **J8_standalone** (beginner-friendly language, llm check): Judge error (fail-closed): daily quota exhausted for this model: {"error":{"message":"Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01m7d2wdmge58sqmf4ewp78bb8` service tier `on_demand` on tokens per day (TPD): Limit 200000, Used 199319, Req
