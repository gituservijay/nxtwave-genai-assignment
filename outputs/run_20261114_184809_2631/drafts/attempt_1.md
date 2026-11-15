# Introduction to RAG

After this lesson, you will know how to use RAG to help an AI answer questions using your own private notes and new documents.

## What is RAG?

RAG stands for Retrieval-Augmented Generation. 
It combines a search step with a large language model. 
A large language model is an AI that reads and writes text like a human. 
In RAG, the system first finds relevant pieces of text from a collection of documents. 
It gives those pieces to the model together with your question. 
The model then writes the answer using that text. 
Patrick Lewis and colleagues at Facebook AI Research introduced this idea in a 2020 research paper. 
The paper is titled "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks". 

Do not think that RAG means the model searches the whole internet by itself. 
It only searches the document collection that the builder connected. 

## Why does RAG matter?

A large language model learns from data up to a cut-off date. 
It does not automatically know new events or documents created after its training. 
Also, it has not seen private documents like a college's rules or your own notes. 
Models can also hallucinate. 
This means they produce answers that sound confident but are wrong or made up. 
Giving the model relevant source text reduces this problem. 
It does not fully remove it. 
RAG lets an application use new or private information without retraining the model. 
Updating the document collection is much cheaper and faster than retraining. 
Because the answer is based on retrieved text, a RAG system can show its sources. 
Then you can check if the answer is correct. 

Some people think that RAG retrains or fine-tunes the model on your documents. 
This is false. 
RAG does not change the model's internal weights. 
It only gives extra text in the prompt at the time of the question. 
Some people also think RAG makes the AI always correct. 
This is also false. 
You should still check answers when it matters. 

## How does RAG work?

Let us use a running example of a college student in India. 
You want to ask questions about your new college fee rules. 
The college gave you a long PDF document with all the rules. 

Step 1: Chunk. 
Documents are split into small pieces called chunks. 
Each chunk is a few paragraphs long. 
For our running example, the fee rule document is split into small chunks of text. 

Step 2: Embed and store. 
Each chunk is converted into an embedding. 
An embedding is a list of numbers that represents the meaning of the text. 
Texts with similar meaning get similar numbers. 
Do not think embeddings are summaries written in words. 
They are just lists of numbers. 
These embeddings are stored in a database built for fast similarity search. 
This is called a vector database. 
Examples of vector databases are FAISS, Chroma, and Pinecone. 
For our running example, every chunk about college fees is turned into a list of numbers and saved in this database. 

Step 3: Retrieve. 
When you ask a question, the question is also converted into an embedding. 
The system finds the chunks whose embeddings are most similar and closest in meaning to your question. 
Usually, the top few chunks are selected. 
Retrieval can also use keyword search, or a mix of keyword and meaning search. 
This is called hybrid search. 
For our running example, you ask, "What is the last date to pay the library fee?" 
The system turns your question into numbers and finds the exact chunk about library fee dates from the database. 

Step 4: Augment. 
The retrieved chunks are added to the prompt together with your question. 
The system gives an instruction to the model, such as "answer using only this context". 
For our running example, the system takes your question and the retrieved chunk about library fees and puts them together. 

Step 5: Generate. 
The language model reads the question plus the retrieved context and writes the answer. 
For our running example, the model reads the text and writes, "The last date to pay the library fee is July 15." 
RAG does not change the model's internal weights during this step. 

Remember that if retrieval finds the wrong or incomplete chunks, the answer can still be wrong. 
Also, the model can only read a limited amount of text at once. 
This limit is its context window. 
So only the most relevant chunks are sent. 

## Worked example

Imagine you are studying at an Indian college and want to know about hostel rules. 
You have a private PDF document with hostel guidelines. 

1. You prepare the knowledge by splitting the PDF into small chunks. 
2. You convert each chunk into an embedding, which is a list of numbers representing meaning. 
3. You store these embeddings in a vector database. 
4. You ask a question: "Can parents stay in the hostel room?" 
5. The system converts your question into an embedding. 
6. It retrieves the most similar chunk from the database, which says: "Visitors and parents are not allowed inside the hostel rooms after 7 PM." 
7. The system augments your question by adding this retrieved chunk to the prompt. 
8. The language model generates the final answer: "No, parents are not allowed inside the hostel rooms after 7 PM, according to your hostel rules." 
9. The system shows the source text so you can check it. 

## Key words

- **Retrieval-Augmented Generation (RAG)** - Combining a search step with a large language model to answer questions using specific documents.
- **Large language model (LLM)** - An AI that reads and writes text like a human.
- **Hallucinate** - When an AI produces answers that sound confident but are wrong or made up.
- **Chunk** - A small piece of a document, such as a few paragraphs.
- **Embedding** - A list of numbers that represents the meaning of a text.
- **Vector database** - A database built for fast similarity search using embeddings.
- **Hybrid search** - A search method that uses both keywords and meaning-based search.
- **Prompt** - The text and instructions given to an AI model when asking a question.
- **Context window** - The limited amount of text a model can read at one time.
- **Fine-tuning** - Changing a model's weights by training it further on examples.

## Recap

- RAG combines a search step with a large language model to answer questions.
- It helps use new or private information without retraining the model.
- Documents are first split into small pieces called chunks.
- Chunks and questions are turned into embeddings, which are lists of numbers representing meaning.
- Embeddings are stored in a vector database for fast similarity search.
- The system retrieves relevant chunks, augments the prompt, and generates an answer.
- RAG reduces hallucinations and lets users check sources, but answers should still be verified.

## Check your understanding

1. Does RAG retrain the model on your private documents?
Answer: No, RAG does not retrain the model. It gives extra text in the prompt at question time.

2. What is an embedding?
Answer: An embedding is a list of numbers that represents the meaning of a text.

3. Can RAG search the entire open internet by itself?
Answer: No, it only searches the document collection that the builder connected.

4. Does RAG completely stop hallucinations and make the AI always correct?
Answer: No, it reduces hallucinations, but you should still check the answers when it matters.
