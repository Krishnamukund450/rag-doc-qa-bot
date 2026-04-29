import streamlit as st
import os
import logging
from dotenv import load_dotenv

# -----------------------------
# Clean logs
# -----------------------------
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
logging.getLogger("transformers").setLevel(logging.ERROR)

load_dotenv()

from src.ingestion import load_documents
from src.chunking import split_documents
from src.vectorstore import create_vectorstore, load_vectorstore
from src.retrieval import get_retriever
from src.generator import generate_answer

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

ul {
    line-height: 1.8;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.title("🤖 AI Document Assistant")
st.caption("Ask questions from your documents — powered by RAG")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("📂 Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("data", exist_ok=True)

    for file in uploaded_files:
        with open(os.path.join("data", file.name), "wb") as f:
            f.write(file.getbuffer())

    st.sidebar.success("✅ Files uploaded")

if st.sidebar.button("📥 Index Documents"):
    with st.sidebar:
        with st.spinner("⚙️ Processing documents..."):
            docs = load_documents("data")
            chunks = split_documents(docs)
            create_vectorstore(chunks)
    st.sidebar.success("🚀 Indexing complete!")

# Clear chat
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

# -----------------------------
# Load DB
# -----------------------------
try:
    vectordb = load_vectorstore()
    retriever = get_retriever(vectordb)
except:
    st.warning("⚠️ Upload & index documents first.")
    st.stop()

# -----------------------------
# Chat History
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Chat Input
# -----------------------------
query = st.chat_input("Ask something...")

if query:
    st.session_state.chat_history.append(("user", query))

    with st.spinner("🤔 Thinking..."):
        docs = retriever.invoke(query)
        answer, sources = generate_answer(query, docs)

    st.session_state.chat_history.append(("bot", answer))
    st.session_state.chat_history.append(("sources", sources))

# -----------------------------
# Display Chat
# -----------------------------
for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.write(message)

    elif role == "bot":
        with st.chat_message("assistant"):
            st.markdown("### 🧠 Answer")
            st.markdown(message)

    elif role == "sources":
        with st.chat_message("assistant"):
            with st.expander("📄 Sources"):
                st.code(message)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with RAG + Ollama + Streamlit")