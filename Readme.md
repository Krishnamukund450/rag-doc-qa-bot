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

## 📄 Source Citations

Each answer includes source citations to show where the information was retrieved from.

- PDF files → show filename and page number  
- DOCX/TXT → show filename only  

This ensures transparency and helps users verify the answers.



---

## ⚙️ Installation & Setup

Follow these steps to set up the project on your system:

### 1. Clone the Repository

```bash
git clone https://github.com/Krishnamukund450/rag-doc-qa-bot.git
cd rag-doc-qa-bot
```
### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Install & Setup Ollama (Local LLM)

Download Ollama from: https://ollama.com

Then pull the required model:
```bash

ollama pull llama3
```
### ▶️ How to Run the Project
Option 1: Run Web UI (Recommended)
```bash
streamlit run streamlit_app.py
```

Open in browser:
http://localhost:8501

Option 2: Run via Command Line
```bash
python app.py
```
---
### 📝 How to Use
1.Upload documents (PDF, TXT, DOCX) using the sidebar (if using UI)
2.Click “Index Documents”
3.Ask questions in the input box
4.View answers along with source citations


---

## 💬 Example Queries

- What is artificial intelligence?
- Explain machine learning
- What is cloud computing?
- Difference between AI and machine learning?
- What is agriculture? → (Expected: I don’t know)

---
### 📂 Requirements
-Python 3.11 or higher
-Ollama installed and running locally
-Internet required only for initial model download

