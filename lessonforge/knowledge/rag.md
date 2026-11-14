# Grounding facts: Retrieval-Augmented Generation (RAG)

This is the reference sheet. The generator teaches only from these facts, and the
evaluator checks every claim in the lesson against them. Each fact has an ID so the judge
can cite which fact a claim matches or contradicts.

## Definition
- F1: RAG stands for Retrieval-Augmented Generation. It combines a search/retrieval step with a large language model (LLM).
- F2: In RAG, before the LLM answers, the system first finds (retrieves) relevant pieces of text from a collection of documents, and gives those pieces to the LLM together with the question. The LLM then writes (generates) the answer using that text.
- F3: The idea was introduced in a 2020 research paper by Patrick Lewis and colleagues at Facebook AI Research (now Meta AI), titled "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".

## Why it matters (problems RAG helps with)
- F4: An LLM learns from data up to a cut-off date. It does not automatically know events or documents created after its training.
- F5: An LLM has not seen private documents (a company's policies, a college's rules, your own notes) unless they are given to it.
- F6: LLMs can "hallucinate": produce answers that sound confident but are wrong or made up. Giving the model relevant source text reduces (but does not fully remove) hallucination.
- F7: RAG lets an application use new or private information without retraining the model. Updating the document collection is usually much cheaper and faster than retraining or fine-tuning.
- F8: Because the answer is based on retrieved text, a RAG system can show its sources, so users can check the answer.

## How it works (the pipeline)
- F9: Step 1 – Prepare the knowledge: documents are split into small pieces called chunks (for example, a few paragraphs each).
- F10: Step 2 – Each chunk is converted into an embedding: a list of numbers that represents the meaning of the text. Texts with similar meaning get similar numbers.
- F11: The embeddings are stored in a database built for fast similarity search, often called a vector database (examples: FAISS, Chroma, Pinecone).
- F12: Step 3 – Retrieve: when a user asks a question, the question is also converted into an embedding, and the system finds the chunks whose embeddings are most similar (closest in meaning). Typically the top few (top-k) chunks are selected.
- F13: Retrieval can also use keyword search, or a mix of keyword and meaning-based search (hybrid search).
- F14: Step 4 – Augment: the retrieved chunks are added to the prompt together with the user's question, with an instruction such as "answer using only this context".
- F15: Step 5 – Generate: the LLM reads the question plus the retrieved context and writes the answer.
- F16: RAG does NOT change the model's internal weights. The model is not retrained; it only receives extra text in its prompt at the time of the question.

## Limits (to stay honest)
- F17: If retrieval finds the wrong or incomplete chunks, the answer can still be wrong ("garbage in, garbage out").
- F18: The LLM can only read a limited amount of text at once (its context window), so only the most relevant chunks are sent.
- F19: RAG reduces hallucination but does not guarantee correct answers; answers should still be checked when it matters.

## RAG vs. fine-tuning (common confusion)
- F20: Fine-tuning changes the model's weights by training it further on examples; it is good for teaching a style or format. RAG gives the model facts at question time; it is good for knowledge that changes often or is private. They can be used together.

## Common real-world uses
- F21: Customer-support chatbots that answer from a company's help documents.
- F22: Assistants that answer questions from a college's or company's internal documents.
- F23: Search assistants that answer with links to their sources.

## Common MISCONCEPTIONS (the lesson must never state these as true)
- M1: "RAG retrains / fine-tunes the model on your documents." (False – see F16.)
- M2: "RAG completely stops hallucinations / makes the AI always correct." (False – see F19.)
- M3: "RAG means the model searches the whole internet by itself." (False – it searches whatever document collection the builder connected; that may or may not include web search.)
- M4: "Embeddings are summaries written in words." (False – they are lists of numbers.)
