# Introduction to RAG

After this lesson, you will be able to explain how RAG helps an AI answer questions using new or private documents without retraining.

## What is RAG?

RAG stands for Retrieval-Augmented Generation. 
It combines a search step with a large language model. 
A large language model is an AI that reads and writes text like ChatGPT. 
In RAG, before the AI answers, the system first finds relevant pieces of text from a collection of documents. 
The system gives those pieces to the AI together with your question. 
Then the AI writes the final answer using that text. 
Patrick Lewis and colleagues at Facebook AI Research introduced this idea in a 2020 research paper. 
The paper is titled "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".

Please note a common mistake. 
RAG does not mean the AI searches the whole internet by itself. 
It only searches the document collection that the builder connected.

## Why does RAG matter?

You might wonder why we need RAG. 
An AI learns from data up to a cut-off date. 
It does not automatically know events or documents created after its training. 
Also, an AI has not seen private documents unless you give them to it. 
Private documents can be a company's policies, a college's rules, or your own notes. 

Without RAG, AIs can make things up. 
This is called hallucination. 
An AI can produce answers that sound confident but are wrong. 
Giving the model relevant source text reduces hallucination. 
However, it does not fully remove it. 
Do not believe the false idea that RAG makes the AI always correct. 
You should still check answers when it matters.

RAG lets an application use new or private information without retraining the model. 
Updating the document collection is usually much cheaper and faster than retraining. 
Because the answer is based on retrieved text, a RAG system can show its sources. 
Then users can check the answer. 

People often confuse RAG with fine-tuning. 
Fine-tuning changes the model by training it further on examples. 
Fine-tuning is good for teaching a style or format. 
RAG gives the model facts at question time. 
RAG does not retrain the model or change its internal weights. 
You can use RAG and fine-tuning together.

Real-world uses include customer-support chatbots that answer from a company's help documents. 
Other uses are assistants that answer questions from a college's internal documents, and search assistants that show sources.

## How does RAG work?

Let us look at the steps. 
We will use a running example of a student named Rahul at a college in India. 
Rahul wants to know the exam fee rules from his college's official PDF guide. 
The college PDF guide is our document collection.

1. Chunk: 
Documents are split into small pieces called chunks. 
A chunk is usually a few paragraphs each. 
For our example, the college PDF guide is split into small chunks, like one chunk for exam fees and another for hostel rules.

2. Embed: 
Each chunk is converted into an embedding. 
An embedding is a list of numbers that represents the meaning of the text. 
Texts with similar meaning get similar numbers. 
Do not think embeddings are summaries written in words. 
They are just lists of numbers. 
The embeddings are stored in a database built for fast similarity search. 
This is called a vector database. 
Examples of vector databases are FAISS, Chroma, and Pinecone. 
For our example, the chunk about exam fees is converted into a list of numbers and stored in the vector database.

3. Retrieve: 
When a user asks a question, the question is also converted into an embedding. 
The system finds the chunks whose embeddings are closest in meaning to the question. 
Typically the top few chunks are selected. 
This is called top-k selection. 
Retrieval can also use keyword search, or a mix of keyword and meaning-based search. 
The mixed search is called hybrid search. 
For our example, Rahul asks, "What is the late fee for exams?" 
The system converts Rahul's question into numbers and finds the exact chunk about exam fees from the college PDF guide. 
Note that if retrieval finds the wrong or incomplete chunks, the answer can still be wrong.

4. Augment: 
The retrieved chunks are added to the prompt together with the user's question. 
The system adds an instruction such as "answer using only this context". 
For our example, the system takes Rahul's question and the exam fee chunk, and puts them together with the instruction to use only that text.

5. Generate: 
The AI reads the question plus the retrieved context and writes the answer. 
For our example, the AI reads the exam fee chunk and tells Rahul the exact late fee amount. 
Remember, RAG does not change the model's internal weights during this time.

## Worked example

Here is how our running example happens from start to end.

- Document: The college publishes a 50-page PDF of rules. Page 12 says the exam late fee is five hundred rupees.
- Step 1 (Chunk): Page 12 is cut into small paragraph chunks.
- Step 2 (Embed and Store): The chunk about exam fees is turned into a list of numbers (an embedding) and stored in a vector database like FAISS.
- Step 3 (Retrieve): Rahul types his question on his smartphone: "What is the exam late fee?" The system turns Rahul's question into numbers. It searches the vector database and retrieves the correct chunk from page 12.
- Step 4 (Augment): The system puts Rahul's question and the page 12 chunk into a prompt. It adds the rule: "Answer using only this context."
- Step 5 (Generate): The large language model reads the prompt and writes the final answer: "The exam late fee is five hundred rupees, according to page 12."
- Source check: The app shows the source as page 12 so Rahul can verify it.

## Key words

- **Large language model** - An AI that reads and writes text like a human.
- **Chunk** - A small piece of a document, like a few paragraphs.
- **Embedding** - A list of numbers that represents the meaning of text.
- **Vector database** - A database built to store embeddings and search them quickly.
- **Hybrid search** - A search method that uses both keywords and meaning.
- **Context window** - The limited amount of text an AI can read at one time.
- **Fine-tuning** - Training a model further on examples to change its weights or style.
- **Hallucination** - When an AI produces answers that sound confident but are wrong or made up.

## Recap

- RAG combines a search step with a large language model to answer questions.
- RAG helps use new or private documents without retraining the AI model.
- Documents are split into chunks, turned into number lists called embeddings, and stored in a vector database.
- When you ask a question, the system retrieves the most similar chunks and adds them to your prompt.
- The AI reads the retrieved text and generates an answer, which helps reduce hallucination.
- RAG systems can show their sources so users can check if the answer is correct.
- RAG does not retrain the model or search the entire internet by itself.

## Check your understanding

1. Does RAG retrain or change the internal weights of the AI model?
Answer: No.

2. What do we call the lists of numbers that represent the meaning of text chunks?
Answer: Embeddings.

3. Can RAG completely stop the AI from making mistakes or hallucinating?
Answer: No.

4. What happens if the retrieval step finds the wrong chunks of text?
Answer: The answer can still be wrong.
