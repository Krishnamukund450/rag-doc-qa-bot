import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

def load_documents(folder_path):
    documents = []

    if not os.path.exists(folder_path):
        raise ValueError(f"Folder not found: {folder_path}")

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        # Skip non-files
        if not os.path.isfile(file_path):
            continue

        try:
            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)

            elif file.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")

            elif file.endswith(".docx"):
                loader = Docx2txtLoader(file_path)

            else:
                print(f"⏭ Skipping unsupported file: {file}")
                continue

            docs = loader.load()
            documents.extend(docs)

            print(f"✅ Loaded: {file} ({len(docs)} pages/chunks)")

        except Exception as e:
            print(f"❌ Error loading {file}: {e}")

    if not documents:
        raise ValueError("No documents were loaded. Check your data folder.")

    return documents