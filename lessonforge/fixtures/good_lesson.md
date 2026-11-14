# Introduction to RAG: How AI Finds the Right Information Before It Answers

After this lesson, you will be able to explain what RAG is, why people use it, and how it works, step by step.

## What is RAG?

First, let us meet the AI tools you already know. ChatGPT is one example. Tools like this are called **large language models**, or **LLMs** for short. An LLM is a computer program that has read a huge amount of text. Because of this, it can answer questions and write sentences like a person.

But an LLM answers from memory. It is like a student writing a **closed-book exam**. The student can only write what they remember.

**RAG** stands for **Retrieval-Augmented Generation**. Let us break the name into three parts:

- **Retrieval** means finding and bringing back. The system first finds useful text for your question.
- **Augmented** means added to or made bigger. The found text is added to your question.
- **Generation** means creating. The LLM then creates (writes) the answer.

So RAG is like an **open-book exam**. Before answering, the AI first opens the right book. It finds the right page. Then it writes the answer using that page.

In one line: **RAG = find the right information first, then let the AI answer using it.**

## Why does RAG matter?

LLMs are very useful. But they have three big problems.

**Problem 1: Old knowledge.** An LLM learns from text up to a certain date. This is called its cut-off date. It does not know about things that happened after that date.

**Problem 2: No private knowledge.** An LLM has not read your college rule book. It has not read a company's private files. It has not read your notes. It only knows these things if someone gives them to it.

**Problem 3: Making things up.** Sometimes an LLM gives an answer that sounds very sure, but it is wrong. This is called **hallucination**. The word means "seeing something that is not there". The AI is not lying on purpose. It is just guessing from patterns.

RAG helps with all three problems:

- It gives the LLM **new and private information** at the moment you ask.
- The LLM answers from real text, so it **makes fewer mistakes**.
- The system can **show its sources**. You can check the page the answer came from.

There is another big benefit. To teach an LLM new things, one way is to train it again. But training again is slow and costs a lot of money. With RAG, you do **not** train the model again. You just add or update your documents. This is much cheaper and faster.

## How does RAG work?

We will use one example in every step.

**Our example:** Your college has a 200-page rule book. It is a PDF file. The college builds a helpdesk chatbot using RAG. You ask the chatbot: *"What is the last date to pay the exam fee?"*

RAG works in two parts. Part A is done once, before anyone asks a question. Part B happens every time someone asks.

**Part A: Prepare the books (done once)**

1. **Cut into chunks.** The rule book is too long to use at once. So it is cut into small pieces. Each piece is called a **chunk**. A chunk may be a few paragraphs long.
   *Example:* One chunk is about hostel rules. Another chunk is about exam fees. Another is about attendance.

2. **Turn each chunk into numbers.** A computer cannot understand meaning the way we do. So each chunk is turned into a long list of numbers. This list is called an **embedding**. Chunks with similar meaning get similar numbers. Think of it like a PIN code for meaning. Places close to each other have close PIN codes. In the same way, texts with close meanings have close numbers.
   *Example:* The exam fee chunk and the "fee payment" chunk get numbers that are close. The hostel food chunk gets very different numbers.

3. **Store them.** All the chunks and their numbers are saved in a special database. It is called a **vector database**. ("Vector" is just another name for a list of numbers.) It is built to quickly find numbers that are close to each other.
   *Example:* All the rule book chunks are now saved and ready to search.

**Part B: Answer a question (every time)**

4. **Retrieve.** Your question is also turned into numbers, in the same way. The system then looks for the chunks with the closest numbers. These chunks are closest in meaning to your question. Usually it picks only the top few. Experts call this "top-k", where k is a small number like 3.
   *Example:* Your question about the exam fee date is turned into numbers. The system finds the exam fee chunk and two other fee chunks.

5. **Augment.** Now the system builds a message for the LLM. The message the LLM reads is called a **prompt**. The prompt has your question plus the chunks that were found. It also has an instruction like: "Answer using only this information."
   *Example:* The prompt says: "Here are three parts of the rule book. Using only these, answer: What is the last date to pay the exam fee?"

6. **Generate.** The LLM reads the prompt and writes the answer.
   *Example:* The chatbot replies: "The last date to pay the exam fee is given in Section 4.2 of the rule book." It also shows that page, so you can check.

One important point: in all these steps, the LLM is **not** trained again. Its brain does not change. It only gets extra reading material inside the prompt, just for your question.

## Worked example

Let us see the full journey once more, from start to end.

1. Before the college opens the chatbot, the rule book is cut into chunks.
2. Each chunk is turned into an embedding, which is a list of numbers.
3. The chunks and embeddings are saved in a vector database.
4. Ravi, a first-year student, types: "What is the last date to pay the exam fee?"
5. His question is turned into numbers. The system finds the three closest chunks. One of them is the exam fee rule.
6. The system builds a prompt. It has Ravi's question, the three chunks, and the instruction "answer only from this".
7. The LLM reads the prompt. It writes a short answer and points to the rule book page.
8. Ravi opens the page and checks the date. He trusts the answer because he can see the source.

Now think: what if the college changes the date next month? They just update the rule book. They make new chunks for the changed part. The chatbot gives the new date. Nobody needs to train the LLM again.

**A warning:** RAG is helpful, but it is not magic. If the system finds the wrong chunk, the answer can still be wrong. Also, an LLM can only read a limited amount of text at one time. This limit is called the **context window**. So only the most useful chunks are sent. RAG reduces mistakes, but it does not remove them fully. For important things, always check the source.

## Key words

- **LLM (large language model)** - a computer program that has read a lot of text and can write answers like a person. Example: ChatGPT.
- **RAG (Retrieval-Augmented Generation)** - find useful text first, add it to the question, then let the LLM write the answer.
- **Retrieval / retrieve** - finding and bringing back useful information.
- **Augment** - to add to something to make it bigger or better.
- **Hallucination** - when an AI gives a wrong or made-up answer that sounds correct.
- **Chunk** - a small piece of a big document.
- **Embedding** - a list of numbers that stands for the meaning of a piece of text.
- **Vector database** - a database that stores embeddings and quickly finds ones that are close in meaning.
- **Top-k** - picking only the best few results, like the top 3.
- **Prompt** - the full message given to an LLM. It has the question and any extra information.
- **Context window** - the limit on how much text an LLM can read at one time.
- **Fine-tuning** - training a model further so its inner settings change. RAG does not do this.

## Recap

- An LLM answers from memory, like a closed-book exam.
- RAG makes it an open-book exam: find the right text first, then answer.
- RAG helps with old knowledge, private documents, and made-up answers.
- The steps are: chunk, embed, store, retrieve, augment, generate.
- RAG does not train the model again. You only update your documents.
- RAG can show its sources, so you can check the answer.
- RAG reduces mistakes, but it does not remove them fully.

## Check your understanding

1. What do the three words in "Retrieval-Augmented Generation" mean?
   Answer: Retrieval means finding useful text. Augmented means adding that text to the question. Generation means the LLM writes the answer.

2. A company changes its leave policy today. Does it need to train its LLM again for its RAG chatbot to know this?
   Answer: No. It only needs to update the document. The new text will be found and given to the LLM.

3. What is an embedding?
   Answer: A list of numbers that stands for the meaning of a piece of text. Similar meanings get similar numbers.

4. Does RAG make an AI always correct?
   Answer: No. If the wrong chunk is found, the answer can still be wrong. RAG reduces mistakes, but you should still check important answers.
