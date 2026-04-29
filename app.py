from dotenv import load_dotenv
load_dotenv()

from src.ingestion import load_documents
from src.chunking import split_documents
from src.vectorstore import create_vectorstore, load_vectorstore
from src.retrieval import get_retriever
from src.generator import generate_answer


def index_data():
    docs = load_documents("data")
    chunks = split_documents(docs)
    create_vectorstore(chunks)
    print("✅ Indexing complete!")


def run_query():
    vectordb = load_vectorstore()
    retriever = get_retriever(vectordb)

    while True:
        query = input("\nAsk a question (type 'exit'): ")

        if query.lower() == "exit":
            break

        docs = retriever.invoke(query)  # ✅ updated (no deprecation warning)
        answer, sources = generate_answer(query, docs)

        print("\n🧠 Answer:\n", answer)
        print("\n📄 Sources:\n", sources)


def main():
    print("\n--- RAG Document Q&A Bot (Final Version) ---")

    while True:
        print("\n1. Index Documents")
        print("2. Ask Questions")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            index_data()
        elif choice == "2":
            run_query()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()