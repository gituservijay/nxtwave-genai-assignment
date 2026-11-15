> **NOT SHIPPED - NEEDS HUMAN REVIEW.** This is the best draft; some checks still fail. See rejection_log.md.

# Introduction to Retrieval-Augmented Generation (RAG)

In this lesson, you will learn how to help a large language model, which is a computer program that understands and writes human text, answer questions using new or private documents without changing the model itself.

## What is RAG?

RAG stands for Retrieval-Augmented Generation. 
It combines a search step with a large language model, which is a computer program that understands and writes human text. 
Before the model answers, the system first finds relevant pieces of text from a collection of documents. 
Then, it gives those pieces to the model together with your question. 
The model writes the answer using that text. 
Patrick Lewis and colleagues at Facebook AI Research introduced this idea in a 2020 research paper. 
They called it Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. 

Do not think that RAG retrains the model on your documents. 
RAG does not change the internal weights, which are the internal numbers the model uses to make decisions. 
Also, RAG does not mean the model searches the whole internet by itself. 
It only searches whatever document collection the builder connected to the system. 

## Why does RAG matter?

A large language model learns from data up to a cut-off date. 
It does not automatically know events or documents created after that time. 
Also, the model has not seen private documents, like your college rules or your own notes, unless you give them to it. 
Sometimes models make mistakes called hallucinations, where they produce answers that sound confident but are wrong or made up. 
Giving the model relevant source text reduces hallucinations, but it does not fully remove them. 

RAG lets an application use new or private information without retraining the model. 
Updating your document collection is much cheaper and faster than retraining. 
Because the answer comes from retrieved text, a RAG system can show its sources so you can check the answer. 

## How does RAG work?

Let us use a running example of a student named Priya. 
Priya studies at a college in India. 
She wants a chatbot to answer questions using her college library fee rulebook. 

Here are the steps the system follows:

1. Chunk - The system prepares the knowledge by splitting documents into small pieces called chunks, such as a few paragraphs each. 
For Priya, the college library rulebook is split into small text chunks. 

2. Embed - Each chunk is converted into an embedding, which is a list of numbers that represents the meaning of the text. 
Texts with similar meaning get similar numbers. 
Do not think embeddings are summaries written in words. 
They are just lists of numbers. 
These embeddings are stored in a database built for fast similarity search, which means a search that finds items that are close in meaning. 
This database is often called a vector database. 
Examples of this database include FAISS, Chroma, and Pinecone. 
For Priya, every rule chunk from the fee book becomes a list of numbers stored in this database. 

3. Retrieve - When a user asks a question, the system converts the question into an embedding too. 
Then it finds the chunks whose embeddings are most similar, meaning they are closest in meaning to the question. 
Typically, the top few chunks are selected. 
Retrieval, which means the act of finding and bringing back relevant pieces of text, can also use keyword search. 
It can also use a mix of keyword and meaning-based search, which is called hybrid search. 
When Priya asks a question about library fine fees, the system converts her question into numbers and finds the exact rule chunks about library fines from the database. 

4. Augment - The retrieved chunks are added to the prompt, which is the text instruction given to the model, together with the user question. 
The system adds an instruction such as "answer using only this context." 
Augment means adding extra source text to the prompt to help the model write a better answer. 
For Priya, the system takes her question about library fines and puts the matching fee rule chunks right next to it with the instruction to use only those rules. 

5. Generate - The large language model reads the question plus the retrieved context and writes the answer. 
The model does not change its internal weights during this time. 
For Priya, the model reads her question and the library fee rules. 
Then the model generates a clear, correct answer about her library dues. 

## Worked example

Here is how Priya uses her college RAG system from start to end. 

Priya types this question into her phone: "What is the late fee for returning a book after ten days?"

Step 1: The system looks at the college library rulebook and breaks it into small paragraphs called chunks. 

Step 2: The system converts each chunk into an embedding, which is a list of numbers representing the meaning, and stores them in a vector database. 

Step 3: The system converts Priya's question into an embedding and retrieves the specific text chunk about library late fees from the database. 

Step 4: The system adds this retrieved text chunk to the prompt along with Priya's question, using the instruction to answer using only that context. 

Step 5: The model reads the question and the context. 
Then the model generates the final answer for Priya. 

Finally, the system shows Priya the answer along with the source document name, so she can verify it. 

## Key words

- **Large language model (LLM)** - A computer program that understands and writes human text.
- **Chunk** - A small piece of text made by splitting a larger document.
- **Embedding** - A list of numbers that represents the meaning of a text.
- **Similarity search** - A search process that finds items that are close in meaning.
- **Vector database** - A database built for fast similarity search using embeddings.
- **Retrieval** - The act of finding and bringing back relevant pieces of text from a collection.
- **Hybrid search** - A search method that uses a mix of keyword search and meaning-based search.
- **Prompt** - The text instruction and information given to a model when asking a question.
- **Augment** - Adding extra source text to the prompt to help the model write a better answer.
- **Internal weights** - The internal numbers a model uses to make decisions, which do not change during RAG.
- **Hallucination** - An incorrect or made-up answer produced by a model that sounds confident.
- **Fine-tuning** - Changing a model's weights by training it further on examples.

## Recap

- RAG stands for Retrieval-Augmented Generation, combining a search step with a large language model. 
- In RAG, the system finds relevant text pieces and gives them to the model along with your question before the model writes an answer. 
- RAG helps models use new or private information without retraining the model. 
- Documents are split into chunks, turned into embeddings, and stored in a vector database for fast similarity search. 
- Retrieved text is added to the prompt to augment the information given to the model. 
- RAG reduces hallucinations and lets systems show their sources, but it does not fully guarantee correct answers. 
- RAG does not retrain the model, and it does not search the whole internet by itself. 

## Check your understanding

1. Does RAG retrain the model on your private documents?
Answer: No, RAG does not retrain the model or change its internal weights. 

2. What is an embedding?
Answer: An embedding is a list of numbers that represents the meaning of the text. 

3. What happens during the augment step in RAG?
Answer: The retrieved text chunks are added to the prompt along with the user question and an instruction. 

4. Does RAG completely stop a model from making mistakes or hallucinating?
Answer: No, RAG reduces hallucinations, but it does not fully remove them or guarantee correct answers.
