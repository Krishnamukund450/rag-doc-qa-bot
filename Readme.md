# 🤖 AI Document Q&A Bot (RAG Pipeline)

This project implements a Retrieval-Augmented Generation (RAG) based Document Question Answering system.  
It allows users to upload documents and ask natural language questions. The system retrieves relevant document chunks and generates accurate, grounded answers with source citations.

---

## 🚀 Features

- Supports PDF, TXT, and DOCX documents
- Chunking with overlap to preserve context
- Embedding using HuggingFace models
- Persistent vector database using ChromaDB
- Local LLM using Ollama (llama3)
- Source citations (file + page when available)
- Streamlit web UI + CLI interface
- Handles unknown queries with “I don’t know”

---

## 🛠 Tech Stack

| Component        | Tool Used |
|----------------|----------|
| Language        | Python 3.11 |
| Framework       | LangChain |
| Embeddings      | HuggingFace (`all-MiniLM-L6-v2`) |
| Vector DB       | ChromaDB |
| LLM             | Ollama (llama3) |
| UI              | Streamlit |
| File Parsing    | PyPDFLoader, TextLoader, Docx2txtLoader |

---


## 📥 Document Ingestion

- Loads documents from `/data` folder
- Supported formats:
  - PDF ✅
  - TXT ✅
  - DOCX ✅
- Extracts text and metadata (filename, page when available)

---

## ✂️ Chunking Strategy

- Method: Recursive Character Text Splitter
- Chunk Size: ~500 characters
- Overlap: ~50–100 characters

**Why?**
- Prevents context loss at boundaries
- Improves retrieval quality
- Ensures meaningful chunks

---

## 🧩 Embedding & Vector Database

- Embedding Model: `all-MiniLM-L6-v2`
- Vector Store: ChromaDB (persistent)

**Why?**
- Lightweight and fast
- Works locally (no API dependency)
- Efficient similarity search

---

## 🔍 Retrieval

- Converts user query into embeddings
- Performs similarity search
- Retrieves top-k chunks (default: k=3)
- These chunks are passed to LLM as context

---

## 🤖 Answer Generation

- LLM: llama3 (via Ollama)
- Uses retrieved context only
- Produces:
  - Structured answers (bullet points)
  - Source citations

**Safety:**
- If answer not found → returns “I don’t know”

---

# 🚀 FINAL STEP

After adding:

```bash
git add README.md
git commit -m "Added instructions section"
git push
