> **NOT SHIPPED - NEEDS HUMAN REVIEW.** This is the best draft; some checks still fail. See rejection_log.md.

# Introduction to RAG (Retrieval-Augmented Generation)

After this lesson, you will be able to explain how RAG helps AI answer questions using private or new documents.

## What is RAG?

RAG stands for **Retrieval-Augmented Generation**. 

It is a technique in AI. It combines a search step with a **Large Language Model (LLM)**. An LLM is a smart computer program that reads and writes text.

Think of an open-book exam in your college. 

If a teacher asks you a question, you do not guess. First, you open your textbook and search for the right page. Second, you read the page and write your answer. 

RAG works in the exact same way for AI:
1. **Retrieval (Search):** The system finds relevant pieces of text from a collection of documents.
2. **Augmented (Added):** The system gives those text pieces to the LLM along with your question.
3. **Generation (Writing):** The LLM reads the text pieces and writes the answer.

In 2020, Patrick Lewis and his team at Facebook AI Research (now Meta AI) introduced this idea. They wrote a research paper titled "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks".

## Why does RAG matter?

Standard AI models have three main problems:

1. **Cut-off date:** An LLM only knows information up to the day its training stopped. It does not know new events or new documents.
2. **Private information:** An LLM has not seen private files. For example, it does not know your college rulebook, your company policy, or your personal notes.
3. **Hallucination:** Sometimes an LLM makes up answers that sound confident but are totally wrong. We call this wrong answer a **hallucination**.

RAG solves these problems! 

Instead of guessing, RAG gives the model the exact source text to read. This reduces hallucination. It lets the AI use new or private facts. 

Updating a collection of documents for RAG is much faster and cheaper than retraining the AI model. Also, a RAG system can show its sources. You can click the source link and check the answer yourself.

RAG is used in many real-world tools:
* Support chatbots that answer from company help pages.
* Assistants that answer questions from college or company files.
* Search assistants that show links to their sources.

### RAG vs. Fine-tuning

Some people think RAG changes the AI model itself. That is a mistake! 

**Fine-tuning** trains the model further to change its internal settings (weights). Fine-tuning is great for teaching the AI a specific style or tone. 

RAG does not change the model's internal weights. RAG simply gives facts to the model at the moment you ask a question. RAG is best for information that changes often or is private.

## How does RAG work?

Let us take one example. Imagine your college has a new 50-page PDF rulebook for exams. You want to ask an AI chatbot: *"What is the passing mark for the math exam?"*

Here are the 5 steps RAG takes to answer you.

### Step 1: Chunking (Prepare the knowledge)
A long document is too big for an AI to read all at once. So, the system splits the college rulebook into small pieces called **chunks**. A chunk is usually a few paragraphs.

*Example:* The 50-page college rulebook is cut into 100 small text chunks.

### Step 2: Embedding and Storing
Next, each chunk is converted into an **embedding**. 

An embedding is NOT a text summary written in words. It is a long list of numbers that represents the meaning of the text. Sentences with similar meanings get similar numbers.

These number lists are stored in a special database called a **vector database**. Examples of vector databases are FAISS, Chroma, and Pinecone.

*Example:* The paragraph about math exam marks becomes a list of numbers. It is saved inside Chroma or Pinecone.

### Step 3: Retrieve (Search)
When you ask your question (*"What is the passing mark for the math exam?"*), the system turns your question into a list of numbers too. 

Then, it searches the vector database. It finds the chunks whose numbers are closest in meaning to your question. This is called similarity search. The system picks the top few best chunks (called **top-k** chunks).

Retrieval can also use keyword search, or a mix of keyword and meaning search. This mix is called **hybrid search**.

*Example:* The system finds Chunk #42 from the rulebook because Chunk #42 talks about math passing marks.

### Step 4: Augment (Add context)
Now, the system prepares a full message (prompt) for the LLM. It combines your question with the retrieved chunks. 

It adds a clear instruction like: *"Answer the question using only this provided text."*

*Example:* The system puts Chunk #42 into the message along with your question about math marks.

### Step 5: Generate (Write answer)
The LLM reads the combined message. It uses the text from Chunk #42 to write a clear answer. 

Remember, the LLM was not retrained. Its internal weights did not change. It just read the text you gave it.

*Example:* The LLM writes: *"According to page 12 of the college rulebook, the passing mark for the math exam is 40 out of 100."*

### Limitations to keep in mind
* **Garbage in, garbage out:** If search finds the wrong chunk, the final answer will be wrong.
* **Context window limit:** An LLM can only read a limited amount of text at one time (its **context window**). So only the best chunks are sent.
* **Not 100% perfect:** RAG reduces hallucinations, but it does not completely remove them. You should still double-check important answers!
* **Private search:** RAG does not mean the AI automatically searches the whole internet by itself. It only searches the documents connected to it.

## Worked example

Let us trace our college rulebook example from start to finish.

1. **Document:** College uploads `Exam_Rules_2024.pdf`.
2. **Step 1 (Chunking):** System cuts the PDF into 100 small chunks.
3. **Step 2 (Embedding & Storing):** System converts all 100 chunks into number lists (embeddings). It stores them in a vector database like FAISS.
4. **User Question:** You type, *"What is the fine for late hall ticket submission?"*
5. **Step 3 (Retrieve):** System converts your question into numbers. It searches FAISS and finds Chunk #15, which talks about hall ticket fees and fines.
6. **Step 4 (Augment):** System creates a prompt:
   > "Instruction: Answer using only the text below.  
   > Text: Chunk #15 (Late hall ticket fee is Rs. 100 per day).  
   > Question: What is the fine for late hall ticket submission?"
7. **Step 5 (Generate):** The LLM reads the prompt and replies: *"The fine for late hall ticket submission is Rs. 100 per day."*

## Key words

* **RAG (Retrieval-Augmented Generation)** - A method where AI searches documents first and then uses that text to write an answer.
* **Large Language Model (LLM)** - An AI model trained on text to understand and generate human language.
* **Hallucination** - When an AI model confidently gives a wrong or made-up answer.
* **Chunk** - A small piece of a larger document, usually a few paragraphs long.
* **Embedding** - A list of numbers that represents the mathematical meaning of a piece of text.
* **Vector database** - A database made to store embeddings and search them quickly based on meaning (examples: FAISS, Chroma, Pinecone).
* **Retrieve** - The step where the system searches and finds relevant chunks for a question.
* **Top-k** - The top number of most relevant text chunks selected by the search.
* **Hybrid search** - A search method that combines keyword matching with meaning-based embedding search.
* **Augment** - The step where retrieved text chunks are added into the prompt alongside the question.
* **Generate** - The final step where the LLM reads the prompt and writes the response.
* **Context window** - The maximum limit of text an LLM can read at one time.
* **Fine-tuning** - Retraining an AI model on extra data to change its internal settings (weights).

## Recap

* RAG stands for Retrieval-Augmented Generation.
* RAG combines searching extra documents with writing by an LLM.
* RAG solves problems like old training data, private documents, and AI hallucinations.
* RAG splits files into small chunks and turns them into number lists called embeddings.
* RAG stores embeddings in vector databases such as FAISS, Chroma, or Pinecone.
* RAG does not retrain or change the internal weights of the AI model.
* RAG reduces wrong answers, but you should still check important facts.

## Check your understanding

**Question 1:** What does RAG do before the LLM writes an answer?  
Answer: It searches and retrieves relevant text chunks from a collection of documents.

**Question 2:** Are embeddings text summaries written in simple English words?  
Answer: No. Embeddings are lists of numbers that represent the meaning of text.

**Question 3:** Does RAG change or retrain the internal weights of the LLM?  
Answer: No. RAG does not retrain the model; it only provides extra text in the prompt at question time.

**Question 4:** Can a RAG system completely stop all AI hallucinations?  
Answer: No. RAG reduces hallucinations, but it does not guarantee 100% correct answers.
