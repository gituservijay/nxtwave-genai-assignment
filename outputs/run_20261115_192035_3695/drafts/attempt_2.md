# Introduction to Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) helps a computer answer questions by searching documents first. After this lesson, you will understand how RAG finds facts and writes answers step by step.

## What is RAG?

First, let us understand what a large language model is. A large language model (LLM) is a computer program trained on a huge amount of text. It can read and write text in human language.

RAG stands for Retrieval-Augmented Generation. It combines two main actions:
1. Retrieval: searching and finding relevant pieces of text from documents.
2. Generation: writing an answer using that found text.

Before the LLM writes an answer, the system finds (retrieves) relevant text from saved documents. It gives that text to the LLM along with your question. The LLM then writes (generates) the answer using that text.

In 2020, Patrick Lewis and his team at Facebook AI Research (now Meta AI) introduced RAG. They wrote a research paper titled "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".

## Why does RAG matter?

A large language model (LLM) has some limits:
- It only knows facts up to its training date cut-off. It does not automatically know new events or documents created after training.
- It has not seen private documents. For example, it does not know your college rules, company policies, or personal notes.
- An LLM can hallucinate.

What is a hallucination? A hallucination is when a model produces an answer that sounds confident but is wrong or made up.

RAG helps solve these limits!

Giving relevant document text to the LLM reduces hallucination. But it does not remove hallucination completely. You should still check answers when they matter.

RAG lets an application use new or private information without retraining the model.

Retraining or fine-tuning changes the model's internal settings, called weights. Fine-tuning means training a model further on examples to change its weights. It is good for teaching a style or format.

Updating a collection of documents for RAG is much cheaper and faster than retraining or fine-tuning.

RAG does not change the model's weights. Instead, it adds extra text into the prompt at question time. A prompt is the input text and instructions given to an LLM.

Because RAG uses retrieved text, it can show its sources. Users can check the source text to verify the answer.

Common real-world uses of RAG include:
- Chatbots for customer support that answer using help documents.
- College or company assistants that answer from private documents.
- Search assistants that give answers along with links to sources.

## How does RAG work?

Let us follow a student named Priya. Priya wants to know the library fee rules at her college. She asks her college chatbot: "What is the fee for late library books?"

Here is how the RAG system works in six steps:

1. Step 1: Chunking
First, the system prepares the college document. It splits the document into small text pieces called chunks. For example, one chunk contains the rule about late library books for Priya's college.

2. Step 2: Embedding
Next, each chunk is converted into an embedding. An embedding is a list of numbers that represents the meaning of the text. Texts with similar meanings get similar numbers. Embeddings are not summaries written in words. The system turns the chunk about library fees into a list of numbers.

3. Step 3: Storing in a vector database
The embeddings are saved in a vector database. A vector database is a database built for fast searching of embeddings by meaning. Examples of vector databases are FAISS, Chroma, and Pinecone. The chunk embedding about Priya's library fee is stored here.

4. Step 4: Retrieval
Priya types her question: "What is the fee for late library books?" The system converts her question into an embedding. It compares her question embedding with stored chunk embeddings in the vector database. It finds the chunks closest in meaning. It picks the top few most relevant chunks. This selection is called top-k retrieval. Retrieval can also use exact words (keyword search) or a mix of both (hybrid search). The system retrieves the specific chunk about library late fees for Priya.

5. Step 5: Augment
To augment means to add extra information. The system adds the retrieved chunk into the prompt for the LLM along with Priya's question. It adds an instruction like: "Answer using only this context." An LLM can only read a limited amount of text at one time. This limit is called its context window. So, only the most relevant chunks are sent.

6. Step 6: Generate
Finally, the LLM reads Priya's question and the retrieved text. It writes (generates) the answer using that text. If retrieval finds the wrong chunks, the answer can still be wrong. But here, it finds the right chunk and answers correctly. The model does not change its internal weights during this step.

## Worked example

Here is the complete story of Priya from start to finish:

1. College document preparation:
The college uploads a 100-page document of rules. The system cuts the document into small chunks. One chunk says: "Students must pay a late fee of 5 rupees per day for overdue library books." The system converts each chunk into an embedding (a list of numbers) and saves them in a vector database.

2. Priya asks a question:
Priya opens the college chatbot on her phone. She types: "What is the fee for late library books?"

3. Retrieval:
The system converts Priya's question into an embedding. It searches the vector database and finds the top chunk about overdue library books.

4. Augment:
The system builds a prompt for the LLM. It combines Priya's question, the retrieved chunk, and an instruction:
Prompt: "Context: Students must pay a late fee of 5 rupees per day for overdue library books. Question: What is the fee for late library books? Instruction: Answer using only this context."

5. Generation:
The LLM reads the prompt. It generates the answer: "The late fee for overdue library books is 5 rupees per day." It also shows the link to the library rule document so Priya can check it.

## Key words

- **Large Language Model (LLM)** - A computer program trained on text to read and write language.
- **Retrieval-Augmented Generation (RAG)** - A system that searches documents first and then generates an answer using an LLM.
- **Retrieval** - Searching and finding relevant text pieces from a collection of documents.
- **Generation** - Writing an answer using an LLM based on retrieved text.
- **Hallucination** - When an LLM produces an answer that sounds confident but is wrong or made up.
- **Weights** - The internal settings of a computer model.
- **Fine-tuning** - Changing a model's internal weights by training it further on examples.
- **Prompt** - The text input and instructions given to an LLM.
- **Chunk** - A small piece of text cut from a larger document.
- **Embedding** - A list of numbers that represents the meaning of a piece of text.
- **Vector database** - A database built to store embeddings and search them quickly by meaning.
- **Top-k** - Selecting the top few most relevant text chunks.
- **Augment** - Adding retrieved text chunks into the prompt given to the LLM.
- **Context window** - The limited amount of text an LLM can read at one time.

## Recap

- RAG stands for Retrieval-Augmented Generation and combines document search with answer generation.
- It was introduced in 2020 by Patrick Lewis and his team at Facebook AI Research (now Meta AI).
- RAG helps an LLM answer questions using new or private documents without retraining the model.
- It reduces hallucinations, but users should still check important facts.
- The pipeline steps are: split text into chunks, convert chunks to embeddings, store embeddings in a vector database, retrieve top-k chunks, augment the prompt, and generate the answer.
- RAG does not change the internal weights of the model.

## Check your understanding

1. What does RAG stand for?
Answer: RAG stands for Retrieval-Augmented Generation.

2. Does RAG change the internal weights of the model?
Answer: No, RAG does not change the model's internal weights. It only adds retrieved text to the prompt at question time.

3. What is an embedding in RAG?
Answer: An embedding is a list of numbers that represents the meaning of a piece of text.

4. What is a hallucination in an LLM?
Answer: A hallucination is when an LLM produces an answer that sounds confident but is wrong or made up.
