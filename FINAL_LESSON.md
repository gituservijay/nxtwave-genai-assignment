# Introduction to Retrieval-Augmented Generation (RAG)

In this lesson, you will learn about Retrieval-Augmented Generation (RAG), a technique where a computer searches documents to help write accurate answers to your questions.

## What is RAG?

RAG stands for Retrieval-Augmented Generation. It is a smart technique used in Artificial Intelligence (AI). Artificial Intelligence (AI) means computer systems built to solve problems and perform smart tasks.

RAG combines a search step with a Large Language Model (LLM). A Large Language Model (LLM) is a smart program trained to read and write text like a human.

To answer a question, the system first finds helpful text pieces from a collection of documents. Finding relevant text pieces from documents is called retrieval. To retrieve means to search and find relevant pieces of text.

Then, it gives those pieces to the LLM along with your question. Finally, the LLM writes an answer based on that text. Writing or producing text using an AI model is called generation. To generate means to write or produce text.

This concept was introduced in a 2020 research paper. It was written by Patrick Lewis and colleagues at Facebook AI Research (now Meta AI). The paper was titled "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".

## Why does RAG matter?

An LLM learns from data up to its training cut-off date. It does not know events or documents created after its training.

An LLM has also not seen your private documents. For example, it does not know your college rules or private study notes.

Without extra help, LLMs can hallucinate. To hallucinate means to produce answers that sound confident but are wrong or made up.

Giving source text to the model reduces hallucination. It does not completely remove mistakes, but it makes answers much more reliable.

RAG lets an application use new or private facts without retraining the model. Retraining means training the AI model all over again from scratch.

Updating a document collection for RAG is cheaper and faster than retraining or fine-tuning. Fine-tuning means training an existing model further on specific examples to change its style or format.

Fine-tuning changes the model weights. Weights are internal number settings that act as the model memory. RAG does not change these internal settings. Instead, it gives facts to the model at question time.

Also, RAG can show its sources. Users can check the source text to verify the answer.

Common real-world uses of RAG include:
- Support chatbots that answer questions from company help documents.
- Student assistants that answer questions from college documents.
- Search tools that show answer text with source links.

## How does RAG work?

Let us follow a student named Anand. Anand wants to know his college hostel entry time from a long college handbook PDF.

Here is how a RAG system works for Anand step by step.

### Step 1: Chunk (Prepare the text)
First, big documents are cut into small text pieces called chunks. A chunk is a small piece of text cut from a larger document, usually a few paragraphs long.

For Anand, the system splits his college handbook into small chunks about hostel rules, library rules, and fees.

### Step 2: Embed and Store
Next, each chunk is turned into an embedding. An embedding is a list of numbers that represents the meaning of a text.

Embeddings are not word summaries. They are purely lists of numbers. Texts with similar meaning get similar numbers.

These embeddings are saved in a vector database. A vector database is a database built for fast searching of text embeddings based on meaning. Examples of vector databases are FAISS, Chroma, and Pinecone.

All chunks from Anand's handbook are now saved as embeddings inside the vector database.

### Step 3: Retrieve (Search)
Anand types his question: "What is the hostel entry time at night?"

The system converts Anand's question into an embedding. It compares his question embedding with the stored chunk embeddings.

The system finds the top-k chunks. Top-k means the top few chunks that are closest in meaning to the question.

Retrieval can also use keyword search. Keyword search looks for exact words or phrases in text documents.

Retrieval can also mix keyword search and meaning search. Mixing keyword search and meaning search is called hybrid search.

The system retrieves the top chunk from the handbook about hostel timings for Anand.

### Step 4: Augment (Add context)
Now, the system builds a prompt. A prompt is the text input message and instructions given to an LLM.

The system adds the retrieved chunk into the prompt together with Anand's question. It includes an instruction such as: "Answer using only this context."

This step is called augment because it adds retrieved source text into the prompt. To augment means to add extra retrieved text to the prompt.

### Step 5: Generate (Write the answer)
The LLM reads the full prompt. It reads Anand's question and the retrieved text chunk.

The LLM writes the final answer for Anand: "The hostel entry time is 9:00 PM."

This writing step is called generate.

Remember, RAG does not change the internal weights (memory settings) of the LLM. The model is not retrained. It simply reads the extra text provided inside the prompt.

### Limits of RAG
- If retrieval finds wrong or incomplete chunks, the answer can still be wrong.
- An LLM has a limited context window. A context window is the maximum amount of text an LLM can read in one message. Only the most relevant chunks are sent.
- RAG reduces hallucination, but it does not guarantee 100 percent correct answers. You should still check answers for important tasks.

## Worked example

Here is the full flow of Anand's question from start to finish:

1. **Document:** College handbook PDF (100 pages).
2. **Chunking:** Handled by splitting the PDF into 300 small text chunks.
3. **Embedding:** Each chunk becomes a list of numbers and is saved in a Chroma vector database.
4. **Question:** Anand asks, "What is the last entry time for the hostel?"
5. **Retrieval:** The system converts Anand's question to numbers. It retrieves the top chunk: "Hostel gates close at 9:00 PM for all students."
6. **Augment:** The system creates this prompt: "Context: Hostel gates close at 9:00 PM for all students. Question: What is the last entry time for the hostel? Instruction: Answer using only this context."
7. **Generate:** The LLM reads the prompt and answers Anand: "The last entry time for the hostel is 9:00 PM."

## Key words

- **Retrieval-Augmented Generation (RAG)** - A system that searches documents first and then uses an LLM to generate an answer.
- **Artificial Intelligence (AI)** - Computer systems built to solve problems and perform smart tasks.
- **Large Language Model (LLM)** - An AI program trained to read and write text like a human.
- **Retrieve / Retrieval** - Searching and finding relevant pieces of text from documents.
- **Generate / Generation** - Writing text output using an AI model.
- **Hallucinate / Hallucination** - When an AI model outputs an answer that sounds confident but is wrong or made up.
- **Retraining** - Training an AI model again from scratch using new data.
- **Fine-tuning** - Training an existing model further on specific examples to change its style or format.
- **Weights** - The internal number settings inside an AI model that store its learned patterns.
- **Chunk** - A small piece of text cut from a larger document.
- **Embedding** - A list of numbers that represents the meaning of a piece of text.
- **Vector database** - A database built for fast searching of embeddings based on meaning.
- **Top-k** - The top few best matching text chunks selected during retrieval.
- **Keyword search** - A search method that looks for exact words or phrases in text documents.
- **Hybrid search** - A search method that combines keyword matching and meaning-based search.
- **Prompt** - The text input message and instructions given to an LLM.
- **Augment** - Adding retrieved source text into the prompt before sending it to the LLM.
- **Context window** - The maximum amount of text an LLM can read in one input message.

## Recap

- RAG combines document retrieval with text generation by an LLM.
- Big documents are split into chunks and saved as numeric embeddings in a vector database.
- When a user asks a question, the system retrieves the closest matching chunks.
- The retrieved text is added to the prompt to help the LLM write a correct answer.
- RAG lets models answer from private or new documents without changing model weights.
- RAG reduces hallucination, but it does not guarantee complete accuracy.
- Updating documents for RAG is faster and cheaper than fine-tuning or retraining.

## Check your understanding

1. Does RAG retrain the LLM or change its internal weights?
Answer: No, RAG does not retrain the model or change its internal weights; it only adds context to the prompt.

2. What is an embedding in a RAG system?
Answer: An embedding is a list of numbers that represents the meaning of a piece of text.

3. What does it mean when an LLM hallucinates?
Answer: Hallucinate means the LLM produces an answer that sounds confident but is wrong or made up.

4. Why are documents split into small chunks before being saved in a vector database?
Answer: Documents are split into chunks because an LLM has a limited context window and can only read a limited amount of text at once.
