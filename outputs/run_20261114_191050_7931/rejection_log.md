# Rejection log - Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `run_20261114_191050_7931`
- **Final status:** **NEEDS_HUMAN_REVIEW** (attempt 3 of max 3)
- **Generator:** `gemini:gemini-3.5-flash-lite`  |  **Judge:** `openai_compat:openai/gpt-oss-120b`  |  LLM calls: 30

**Rules learned from earlier runs (added to the writer prompt):**

  - [J5_jargon_explained] Define every technical acronym or jargon term in plain language immediately upon its first appearance in the text.
  - [D6_glossary_coverage] Ensure all core technical terms used in the text (such as prompt, retrieval, and augment) are explicitly listed in the Key words glossary.
  - [J4_teaches_by_example] Integrate the designated running example character consistently across every single step and phase of the main mechanism explanation.

## Score per attempt

| Check | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|
| D1_structure | PASS | PASS | PASS |
| D2_length | PASS | PASS | PASS |
| D3_sentence_length | **FAIL** | PASS | **FAIL** |
| D4_readability | PASS | PASS | PASS |
| D5_hard_words | PASS | PASS | PASS |
| D6_glossary_coverage | **FAIL** | PASS | PASS |
| D7_quiz | PASS | PASS | PASS |
| J1_accurate | PASS | PASS | PASS |
| J2_grounded | **FAIL** | **FAIL** | PASS |
| J3_key_points | PASS | PASS | PASS |
| J4_teaches_by_example | PASS | PASS | PASS |
| J5_jargon_explained | **FAIL** | **FAIL** | **FAIL** |
| J6_language_fit | PASS | PASS | PASS |
| J7_flow | PASS | PASS | PASS |
| J8_standalone | PASS | PASS | PASS |
| **Total** | **11/15** | **13/15** | **13/15** |

## Attempt 1 - REJECTED (11/15)

**What failed and why:**

- **D3_sentence_length** (beginner-friendly language, code check): Average 15.5 words/sentence (max 16); 1 sentence(s) over 30 words
  - Evidence: _Step 5: The model reads the question and the context, and generates the final answer: "According to your library rulebook, the late fee is ten rupees per day after the due date."_
  - Fix requested: Split every long sentence into two or three short ones. One idea per sentence.
- **D6_glossary_coverage** (clear, no unexplained jargon, code check): Used but not in Key words: retrieval, augment
  - Fix requested: Add simple one-line meanings for: retrieval, augment in the Key words section.
- **J2_grounded** (accurate & grounded, llm check): The lesson mentions a vector database named "FAIPS", which is not listed in the reference facts (the correct name is FAISS).
  - Evidence: _"Examples of this database include FAIPS, Chroma, and Pinecone."_
  - Fix requested: Replace "FAIPS" with the correct product name "FAISS" as given in the reference facts.
- **J5_jargon_explained** (clear, no unexplained jargon, llm check): The term "similarity search" is used before it is explained.
  - Evidence: _"These embeddings are stored in a database built for fast similarity search, often called a vector database."_
  - Fix requested: Add a simple explanation of "similarity search" (e.g., "a similarity search finds items that are close in meaning") before or immediately after its first appearance.

## Attempt 2 - REJECTED (13/15)

**What changed on this retry (feedback sent to the writer):**

```
- [D3_sentence_length] Average 15.5 words/sentence (max 16); 1 sentence(s) over 30 words
  Evidence: Step 5: The model reads the question and the context, and generates the final answer: "According to your library rulebook, the late fee is ten rupees per day after the due date."
  Fix: Split every long sentence into two or three short ones. One idea per sentence.
- [D6_glossary_coverage] Used but not in Key words: retrieval, augment
  Evidence: -
  Fix: Add simple one-line meanings for: retrieval, augment in the Key words section.
- [J2_grounded] The lesson mentions a vector database named "FAIPS", which is not listed in the reference facts (the correct name is FAISS).
  Evidence: "Examples of this database include FAIPS, Chroma, and Pinecone."
  Fix: Replace "FAIPS" with the correct product name "FAISS" as given in the reference facts.
- [J5_jargon_explained] The term "similarity search" is used before it is explained.
  Evidence: "These embeddings are stored in a database built for fast similarity search, often called a vector database."
  Fix: Add a simple explanation of "similarity search" (e.g., "a similarity search finds items that are close in meaning") before or immediately after its first appearance.
```

**What failed and why:**

- **J2_grounded** (accurate & grounded, llm check): The lesson makes a factual claim not covered by the reference facts.
  - Evidence: _"RAG does not search the whole internet by itself unless connected to web search."_
  - Fix requested: Remove the unsupported clause "unless connected to web search" or rephrase to match the reference fact that RAG does not search the whole internet by itself.
- **J5_jargon_explained** (clear, no unexplained jargon, llm check): The term "large language model" is used before it is explained.
  - Evidence: _"In this lesson, you will learn how to help a **large language model** answer questions..." (first use) – the explanation "large language model, which is a computer program that understands and writes human text" appears later, not at or before the first use._
  - Fix requested: Introduce a simple definition of each technical term (e.g., "large language model – a computer program that understands and writes human text") before its first occurrence in the lesson.

## Attempt 3 - REJECTED (13/15)

**What changed on this retry (feedback sent to the writer):**

```
- [J2_grounded] The lesson makes a factual claim not covered by the reference facts.
  Evidence: "RAG does not search the whole internet by itself unless connected to web search."
  Fix: Remove the unsupported clause "unless connected to web search" or rephrase to match the reference fact that RAG does not search the whole internet by itself.
- [J5_jargon_explained] The term "large language model" is used before it is explained.
  Evidence: "In this lesson, you will learn how to help a **large language model** answer questions..." (first use) – the explanation "large language model, which is a computer program that understands and writes human text" appears later, not at or before the first use.
  Fix: Introduce a simple definition of each technical term (e.g., "large language model – a computer program that understands and writes human text") before its first occurrence in the lesson.
```

**Regressions** (passed before, failed now): D3_sentence_length

**What failed and why:**

- **D3_sentence_length** (beginner-friendly language, code check): Average 15.0 words/sentence (max 16); 1 sentence(s) over 30 words
  - Evidence: _In this lesson, you will learn how to help a large language model, which is a computer program that understands and writes human text, answer questions using new or private documents without changing the model itself._
  - Fix requested: Split every long sentence into two or three short ones. One idea per sentence.
- **J5_jargon_explained** (clear, no unexplained jargon, llm check): The term "Fine-tuning" is first introduced in the Key words section without any prior explanation in the main body.
  - Evidence: _"- **Fine-tuning** - Changing a model's weights by training it further on examples."_
  - Fix requested: Introduce a simple explanation of "Fine-tuning" in the main lesson text before it appears in the Key words list, e.g., "Fine-tuning means changing a model's internal weights by training it further on example data."
