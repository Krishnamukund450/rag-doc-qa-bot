from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

PERSIST_DIR = "db"


def create_vectorstore(chunks):
    if not chunks:
        raise ValueError("No chunks found.")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    BATCH_SIZE = 100

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        vectordb.add_documents(batch)
        print(f"Indexed batch {i//BATCH_SIZE + 1}")

    return vectordb


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )