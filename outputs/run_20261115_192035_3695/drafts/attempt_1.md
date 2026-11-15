# Introduction to Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) helps a computer answer questions by finding facts in documents first. After this lesson, you can explain how RAG finds facts and answers questions step by step.

## What is RAG?

First, what is a large language model (LLM)? An LLM is a computer program trained on lots of text to read and write language.

RAG stands for Retrieval-Augmented Generation. It combines two main steps:
1. Retrieval: searching and finding relevant text from documents.
2. Generation: writing an answer using that text.

Before the LLM answers, the system finds (retrieves) relevant pieces of text from saved documents. It gives those text pieces to the LLM along with your question. The LLM then writes (generates) the answer using that text.

Patrick Lewis and his team at Facebook AI Research (now Meta AI) introduced RAG. They wrote a research paper in 2020. The paper was titled "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".

## Why does RAG matter?

An LLM has some limits:
- It only knows data up to its training date.
- It has not seen private documents, like your college rules or personal notes.
- An LLM can hallucinate.

Hallucination means the model gives an answer that sounds confident but is wrong or made up.

RAG helps solve these problems!

Giving relevant text to the model reduces hallucination. It does not completely stop hallucination. You should still check important answers.

RAG uses new or private information without retraining the model. Retraining or fine-tuning changes the model's internal settings, called weights. Fine-tuning teaches a style or format by training on examples. Updating documents for RAG is much cheaper and faster than retraining.

RAG does not change the model's internal weights. It puts extra text into the prompt at question time. A prompt is the input text and instructions given to an LLM.

Because RAG uses retrieved text, it can show its sources. Users can check the source to verify the answer.

Common real-world uses of RAG include:
- Customer-support chatbots that answer using help documents.
- College or company assistants that answer from private documents.
- Search assistants that show answers with links to sources.

## How does RAG work?

Imagine a student named Priya. She wants to know the library fee rules at her college. The college uses a RAG system to answer her.

Here is how the system works:

1. Chunking:
Documents are cut into small text pieces called chunks. For example, a chunk can be a few
