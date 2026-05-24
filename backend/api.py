from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os

from dotenv import load_dotenv

load_dotenv()

from src.ingestion import load_documents
from src.chunking import split_documents
from src.vectorstore import create_vectorstore, load_vectorstore
from src.retrieval import get_retriever
from src.generator import generate_answer


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Config
# -----------------------------
DATA_PATH = os.getenv("DATA_PATH", "data")

# -----------------------------
# Upload Endpoint
# -----------------------------
@app.post("/upload")

async def upload_file(file: UploadFile = File(...)):

    os.makedirs(DATA_PATH, exist_ok=True)

    file_path = os.path.join(DATA_PATH, file.filename)

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    return {
        "message": f"{file.filename} uploaded successfully"
    }

# -----------------------------
# Index Endpoint
# -----------------------------
@app.post("/index")

def index_documents():

    docs = load_documents(DATA_PATH)

    chunks = split_documents(docs)

    create_vectorstore(chunks)

    return {
        "message": "Documents indexed successfully"
    }

# -----------------------------
# Ask Endpoint
# -----------------------------
@app.post("/ask")

def ask_question(query: dict):

    question = query["question"]

    vectordb = load_vectorstore()

    retriever = get_retriever(vectordb)

    docs = retriever.invoke(question)

    answer, sources = generate_answer(
        question,
        docs
    )

    return {
        "answer": answer,
        "sources": sources
    }

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")

def root():

    return {
        "message": "RAG API is running"
    }