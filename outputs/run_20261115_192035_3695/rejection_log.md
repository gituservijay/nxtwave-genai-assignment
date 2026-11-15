# Rejection log - Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `run_20261115_192035_3695`
- **Final status:** **NEEDS_HUMAN_REVIEW** (attempt 3 of max 3)
- **Generator:** `gemini:gemini-3.6-flash`  |  **Judge:** `openai_compat:openai/gpt-oss-120b`  |  LLM calls: 29

**Rules learned from earlier runs (added to the writer prompt):**

  - [J5_jargon_explained] Define every technical term or keyword in plain language in the main body text before using it anywhere else, including the Key words section.
  - [D6_glossary_coverage] List every technical term used in the lesson—such as prompt, retrieval, augment, and top-k—in the Key words glossary.
  - [D3_sentence_length] Keep all sentences under 25 words and maintain an average sentence length below 14 words by breaking up compound clauses.
  - [J2_grounded] Strictly verify proper nouns, acronyms, and factual claims against the reference facts without altering or inventing details.
  - [J4_teaches_by_example] Integrate the designated running example character consistently across every single step and phase of the main mechanism explanation.

## Score per attempt

| Check | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|
| D1_structure | **FAIL** | PASS | PASS |
| D2_length | **FAIL** | PASS | PASS |
| D3_sentence_length | PASS | PASS | PASS |
| D4_readability | PASS | PASS | PASS |
| D5_hard_words | PASS | PASS | PASS |
| D6_glossary_coverage | **FAIL** | PASS | PASS |
| D7_quiz | **FAIL** | PASS | PASS |
| J1_accurate | PASS | PASS | PASS |
| J2_grounded | PASS | PASS | **FAIL** |
| J3_key_points | **FAIL** | PASS | PASS |
| J4_teaches_by_example | **FAIL** | PASS | PASS |
| J5_jargon_explained | PASS | **FAIL** | **FAIL** |
| J6_language_fit | PASS | **FAIL** | PASS |
| J7_flow | **FAIL** | PASS | PASS |
| J8_standalone | PASS | PASS | PASS |
| **Total** | **8/15** | **13/15** | **13/15** |

## Attempt 1 - REJECTED (8/15)

**What failed and why:**

- **D1_structure** (coherent teaching flow, code check): Missing sections: example, keywords, recap, quiz
  - Evidence: _Found H2 headings: ['what is rag', 'why does rag matter', 'how does rag work']_
  - Fix requested: Use exactly these H2 sections in order: What is RAG? / Why does RAG matter? / How does RAG work? / Worked example / Key words / Recap / Check your understanding.
- **D2_length** (covers the key points, code check): 392 words (allowed 700-2000)
  - Fix requested: Add more explanation and examples.
- **D6_glossary_coverage** (clear, no unexplained jargon, code check): Used but not in Key words: LLM / large language model, chunk, prompt, retrieval, hallucination, fine-tuning, augment
  - Fix requested: Add simple one-line meanings for: LLM / large language model, chunk, prompt, retrieval, hallucination, fine-tuning, augment in the Key words section.
- **D7_quiz** (teaches by example, code check): 0 question(s), 0 answer(s) (need >= 3, each answered)
  - Fix requested: Add at least 3 short questions, each followed by a line starting with 'Answer:'.
- **J3_key_points** (covers the key points, llm check): The lesson does not cover the full pipeline steps (embed → store → retrieve → augment → generate) after chunking.
  - Evidence: _The lesson stops at "1. Chunking: Documents are cut into small text pieces called chunks. For example, a chunk can be a few" and never mentions embedding, storing, retrieval, augmentation, or generation steps._
  - Fix requested: Add a clear description of the remaining pipeline: (b) converting each chunk into an embedding, (c) storing embeddings in a vector database, (d) retrieving relevant chunks for a query, (e) augmenting the prompt with those chunks, and (f) generating the answer with the LLM.
- **J4_teaches_by_example** (teaches by example, llm check): The lesson introduces the example of Priya only in the first step and does not show the example in the subsequent steps of the RAG pipeline.
  - Evidence: _"Imagine a student named Priya..." appears only in the first listed step (Chunking) and later steps are missing or do not reference Priya._
  - Fix requested: Add the same running example (Priya) to every step of the 'How does RAG work?' section (retrieval, augment, generate, etc.) and ensure each step includes her context.
- **J7_flow** (coherent teaching flow, llm check): The lesson lacks a recap section that summarizes what was taught, violating the requirement that the recap matches the lesson content.
  - Evidence: _The provided lesson ends with the start of the 'How does RAG work?' section and does not contain any recap summarizing the previous sections._
  - Fix requested: Add a final recap section that briefly restates the definition of RAG, why it matters, and the main steps of the RAG pipeline, ensuring it aligns with the material presented.

## Attempt 2 - REJECTED (13/15)

**What changed on this retry (feedback sent to the writer):**

```
- [D1_structure] Missing sections: example, keywords, recap, quiz
  Evidence: Found H2 headings: ['what is rag', 'why does rag matter', 'how does rag work']
  Fix: Use exactly these H2 sections in order: What is RAG? / Why does RAG matter? / How does RAG work? / Worked example / Key words / Recap / Check your understanding.
- [D2_length] 392 words (allowed 700-2000)
  Evidence: -
  Fix: Add more explanation and examples.
- [D6_glossary_coverage] Used but not in Key words: LLM / large language model, chunk, prompt, retrieval, hallucination, fine-tuning, augment
  Evidence: -
  Fix: Add simple one-line meanings for: LLM / large language model, chunk, prompt, retrieval, hallucination, fine-tuning, augment in the Key words section.
- [D7_quiz] 0 question(s), 0 answer(s) (need >= 3, each answered)
  Evidence: -
  Fix: Add at least 3 short questions, each followed by a line starting with 'Answer:'.
- [J3_key_points] The lesson does not cover the full pipeline steps (embed → store → retrieve → augment → generate) after chunking.
  Evidence: The lesson stops at "1. Chunking: Documents are cut into small text pieces called chunks. For example, a chunk can be a few" and never mentions embedding, storing, retrieval, augmentation, or generation steps.
  Fix: Add a clear description of the remaining pipeline: (b) converting each chunk into an embedding, (c) storing embeddings in a vector database, (d) retrieving relevant chunks for a query, (e) augmenting the prompt with those chunks, and (f) generating the answer with the LLM.
- [J4_teaches_by_example] The lesson introduces the example of Priya only in the first step and does not show the example in the subsequent steps of the RAG pipeline.
  Evidence: "Imagine a student named Priya..." appears only in the first listed step (Chunking) and later steps are missing or do not reference Priya.
  Fix: Add the same running example (Priya) to every step of the 'How does RAG work?' section (retrieval, augment, generate, etc.) and ensure each step includes her context.
- [J7_flow] The lesson lacks a recap section that summarizes what was taught, violating the requirement that the recap matches the lesson content.
  Evidence: The provided lesson ends with the start of the 'How does RAG work?' section and does not contain any recap summarizing the previous sections.
  Fix: Add a final recap section that briefly restates the definition of RAG, why it matters, and the main steps of the RAG pipeline, ensuring it aligns with the material presented.
```

**Regressions** (passed before, failed now): J5_jargon_explained, J6_language_fit

**What failed and why:**

- **J5_jargon_explained** (clear, no unexplained jargon, llm check): The term RAG is used before it is explained, and the term prompt is used before any explanation (the key‑words list does not count).
  - Evidence: _"Retrieval-Augmented Generation (RAG) helps a computer answer questions by searching documents first."; "The system adds the retrieved chunk into the prompt for the LLM along with Priya's question."_
  - Fix requested: Introduce a simple definition of Retrieval‑Augmented Generation (RAG) before its first use, e.g., "Retrieval‑Augmented Generation (RAG) is a method that first searches a set of documents for relevant information and then uses that information to generate an answer." Also define "prompt" before it appears, e.g., "A prompt is the text and instructions that are sent to the language model as input."
- **J6_language_fit** (beginner-friendly language, llm check): The lesson includes a reference to Facebook/Meta, a Western company, which may require US cultural knowledge.
  - Evidence: _"In 2020, Patrick Lewis and his team at Facebook AI Research (now Meta AI) introduced RAG."_
  - Fix requested: Replace the specific mention of Facebook/Meta with a generic description like "a research lab" or "a leading AI research organization".

## Attempt 3 - REJECTED (13/15)

**What changed on this retry (feedback sent to the writer):**

```
- [J5_jargon_explained] The term RAG is used before it is explained, and the term prompt is used before any explanation (the key‑words list does not count).
  Evidence: "Retrieval-Augmented Generation (RAG) helps a computer answer questions by searching documents first."; "The system adds the retrieved chunk into the prompt for the LLM along with Priya's question."
  Fix: Introduce a simple definition of Retrieval‑Augmented Generation (RAG) before its first use, e.g., "Retrieval‑Augmented Generation (RAG) is a method that first searches a set of documents for relevant information and then uses that information to generate an answer." Also define "prompt" before it appears, e.g., "A prompt is the text and instructions that are sent to the language model as input."
- [J6_language_fit] The lesson includes a reference to Facebook/Meta, a Western company, which may require US cultural knowledge.
  Evidence: "In 2020, Patrick Lewis and his team at Facebook AI Research (now Meta AI) introduced RAG."
  Fix: Replace the specific mention of Facebook/Meta with a generic description like "a research lab" or "a leading AI research organization".
```

**Regressions** (passed before, failed now): J2_grounded

**What failed and why:**

- **J2_grounded** (accurate & grounded, llm check): The lesson contains specific factual claims that are not supported by the reference facts.
  - Evidence: _"A model can only read a limited amount of text at one time. This limit is called its context window." (no reference fact about context windows) and "The college uploads a 100-page document of rules." (the number 100 pages is not in the grounding facts)._
  - Fix requested: Remove or rephrase unsupported specific details (e.g., omit the exact page count and the mention of a context window) or add supporting reference facts for those claims.
- **J5_jargon_explained** (clear, no unexplained jargon, llm check): The term "weights" is used before it is explained.
  - Evidence: _"Retraining or fine-tuning changes the model's internal settings, called weights."_
  - Fix requested: Add a simple definition for "weights" (e.g., "Weights are the internal numbers that determine how the model processes information") before or in the same sentence where the term first appears.
