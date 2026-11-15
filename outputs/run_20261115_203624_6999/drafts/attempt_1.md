# Retrieval-Augmented Generation (RAG): A Simple Guide to How AI Finds Facts Before Answering

After reading this lesson, you will understand how Retrieval-Augmented Generation (RAG) helps a computer program search for real information before writing an answer.

## What is RAG?

Retrieval-Augmented Generation (RAG) is a method used in artificial intelligence. It combines a search step with a smart computer program called a Large Language Model (LLM).

A model is a computer program trained on data to perform tasks. A Large Language Model (LLM) is a model trained on lots of text so it can understand and write human-like words.

The name RAG has three parts:
- **Retrieve**: To search and find relevant text pieces from a collection of documents.
- **Augment**: To add those text pieces to your question.
- **Generate**: To write the final answer.

In RAG, the system first finds relevant text pieces from documents. It gives those pieces to the LLM together with your question. The LLM then writes the answer using that text.

This idea was introduced in a 2020 research paper by Patrick Lewis and his colleagues at Facebook AI Research (now called Meta AI). The paper was titled "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".

## Why does RAG matter?

An LLM learns from data up to a cut-off date. It does not know new events or documents created after its training.

An LLM also has not seen private documents. It does not know a college's rules, a company's policies, or your personal notes unless you provide them.

Sometimes, an LLM can hallucinate. To hallucinate means the model produces answers that sound confident but are wrong or made up. Giving the model relevant source text reduces hallucination. It does not fully remove the problem, but it helps a lot.

RAG lets an application use new or private information without retraining the model. Retraining or fine-tuning means changing a model's internal settings, also called weights, by training it further on examples. Fine-tuning is good for teaching a specific writing style or format.

Updating a document collection for RAG is usually much cheaper and faster than retraining or fine-tuning a model. RAG does not change the model's weights (internal settings). The model only receives extra text in its prompt at question time. A prompt is the input text or question you give to the model.

Because the answer is based on retrieved text, a RAG system can show its sources. Users can then check the original documents to verify the answer.

Common real-world uses of RAG include:
- Customer-support chatbots that answer questions from company help files.
- Assistants that answer questions from internal college or company documents.
- Search tools that write answers and provide links to their sources.

## How does RAG work?

To see how RAG works, let us follow a student named Ravi. Ravi wants to know his college fee payment deadline from a 50-page college rulebook.

1. **Chunk**: The system splits large documents into small pieces called chunks. A chunk is usually a few paragraphs.
*Ravi's example:* The system takes the 50-page college rulebook and splits it into small paragraph chunks.

2. **Embed and Store**: Each chunk is converted into an embedding. An embedding is a list of numbers that represents the meaning of the text. Texts with similar meaning get similar numbers. Note that embeddings are lists of numbers, not summaries written in words. The system saves these embeddings in a vector database. A vector database is a special database built for fast similarity search of number lists (examples: FAISS, Chroma, Pinecone).
*Ravi's example:* The system converts each chunk of Ravi's college rulebook into a list of numbers and stores them in a vector database.

3. **Retrieve**: When a user asks a question, the question is also converted into an embedding. The system finds the chunks whose embeddings are closest in meaning to the question. It picks the top few closest pieces, called top-k chunks. Search can also use exact keywords, or a mix of keywords and meaning called hybrid search. Note that RAG does not search the whole internet by itself; it only searches the document collection given to it.
*Ravi's example:* Ravi types the question: "What is the last date to pay college fees?" The system turns Ravi's question into an embedding. It retrieves the top-k chunks about fee dates from the vector database.

4. **Augment**: The system adds the retrieved chunks into the user's prompt alongside the question. It includes an instruction such as "answer using only this context". The total text must fit inside the model's context window. A context window is the maximum amount of text an LLM can read at one time.
*Ravi's example:* The system combines the retrieved fee chunks with Ravi's question into a single prompt.

5. **Generate**: The LLM reads the question plus the retrieved context. It writes the answer using that information. The model's weights (internal settings) do not change during this process.
*Ravi's example:* The LLM reads the combined prompt and writes a clear answer telling Ravi his fee deadline.

## Worked example

Here is the full story of Ravi getting his answer using RAG, from start to finish:

- **Source File**: A 50-page PDF document containing all college rules.
- **Step 1 (Chunk)**: The system splits the 50-page PDF into small text chunks.
- **Step 2 (Embed & Store)**: The system converts every chunk into an embedding (a list of numbers) and saves them in Chroma.
- **Step 3 (Retrieve)**: Ravi types into the computer: "What is the last date to submit college fees?" The system converts Ravi's question into an embedding. It uses similarity search to find the top-k chunks containing fee deadline information.
- **Step 4 (Augment)**: The system creates a prompt: "Context: College fees for the term must be paid by August 31. Question: What is the last date to submit college fees? Answer using only this context."
- **Step 5 (Generate)**: The LLM reads the prompt. It generates the final response: "The last date to submit college fees is August 31."

Keep in mind: If retrieval finds wrong or incomplete chunks, the answer can still be wrong. RAG reduces hallucinations, but it does not guarantee correct answers every time. You should always check important answers!

## Key words

- **Retrieval-Augmented Generation (RAG)** - A technique that combines document search with a Large Language Model to answer questions using retrieved facts.
- **Large Language Model (LLM)** - A computer program trained on large amounts of text to understand and generate human-like words.
- **Model** - A computer program trained on data to complete tasks.
- **Weights** - The millions of internal number settings inside a model that act as its memory settings.
- **Retrieve** - To search for and find relevant text pieces from a collection of documents.
- **Augment** - To add retrieved text pieces into a user's prompt before sending it to a model.
- **Generate** - To write or produce text as an answer.
- **Prompt** - The input text or question given to a model.
- **Hallucination** - When a model produces a wrong or made-up answer that sounds confident.
- **Fine-tuning** - Retraining a model on new examples to change its internal settings (weights) for a specific style or format.
- **Chunk** - A small piece of text split from a larger document, such as a few paragraphs.
- **Embedding** - A list of numbers that represents the meaning of a piece of text.
- **Vector database** - A specialized database built for fast similarity search of embeddings, such as FAISS, Chroma, or Pinecone.
- **Top-k** - The top few chunks whose embeddings are closest in meaning to the user's question.
- **Hybrid search** - A search method that combines keyword search and meaning-based search.
- **Context window** - The limited amount of text an LLM can read at one time.

## Recap

- RAG stands for Retrieval-Augmented Generation, introduced in 2020 by Patrick Lewis and colleagues at Facebook AI Research (now Meta AI).
- RAG finds relevant text pieces from documents and gives them to an LLM to generate an answer.
- Documents are split into chunks and stored as embeddings (lists of numbers) in a vector database like FAISS, Chroma, or Pinecone.
- When a user asks a question, RAG retrieves the top-k most relevant chunks using meaning search, keyword search, or hybrid search.
- RAG does not change the model's weights (internal settings) or retrain the model.
- RAG allows an LLM to use new or private information, shows sources, and reduces hallucinations.
- If retrieval gets incorrect chunks, the answer can still be wrong, so important answers should be checked.

## Check your understanding

1. Does RAG retrain the model or change its internal weights?
Answer: No. RAG does not retrain the model or change its weights; it only adds retrieved context to the prompt at question time.

2. What is an embedding in a RAG system?
Answer: An embedding is a list of numbers that represents the meaning of a piece of text.

3. Why are documents split into small chunks before being sent to an LLM?
Answer: Documents are split into chunks because an LLM has a limited context window and can only read a limited amount of text at once.

4. Does RAG guarantee that the model will never give a wrong answer?
Answer: No. RAG reduces hallucinations, but if the retrieval step gets wrong or incomplete chunks, the final answer can still be wrong.
