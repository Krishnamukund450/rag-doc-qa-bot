from dotenv import load_dotenv
load_dotenv()

from src.ingestion import load_documents
from src.chunking import split_documents
from src.vectorstore import create_vectorstore
import os

DATA_PATH = os.getenv("DATA_PATH", "data")

print("✅ Backend container started successfully")

# Optional startup indexing
if os.path.exists(DATA_PATH):

    try:
        docs = load_documents(DATA_PATH)

        chunks = split_documents(docs)

        create_vectorstore(chunks)

        print("✅ Documents indexed successfully")

    except Exception as e:

        print(f"Indexing skipped: {e}")

# Keep container alive
while True:
    pass