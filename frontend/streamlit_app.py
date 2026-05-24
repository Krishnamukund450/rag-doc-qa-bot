import streamlit as st
import requests

import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

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

st.caption(
    "Ask questions from your documents — powered by FastAPI + Ollama"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("📂 Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF, TXT, DOCX",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True
)

# -----------------------------
# Upload Files
# -----------------------------
if uploaded_files:

    for file in uploaded_files:

        response = requests.post(
            f"{API_URL}/upload",
            files={
                "file": (
                    file.name,
                    file.getvalue()
                )
            }
        )

    st.sidebar.success("✅ Files uploaded successfully")

# -----------------------------
# Index Documents
# -----------------------------
if st.sidebar.button("📥 Index Documents"):

    with st.sidebar:

        with st.spinner("⚙️ Processing documents..."):

            response = requests.post(
                f"{API_URL}/index"
            )

    st.sidebar.success("🚀 Indexing complete!")

# -----------------------------
# Clear Chat
# -----------------------------
if st.sidebar.button("🧹 Clear Chat"):

    st.session_state.chat_history = []

# -----------------------------
# Chat History
# -----------------------------
if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# -----------------------------
# Chat Input
# -----------------------------
query = st.chat_input(
    "Ask something about your documents..."
)

if query:

    st.session_state.chat_history.append(
        ("user", query)
    )

    with st.spinner("🤔 Thinking..."):

        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": query
            }
        )

        data = response.json()

        answer = data["answer"]

        sources = data["sources"]

    st.session_state.chat_history.append(
        ("bot", answer)
    )

    st.session_state.chat_history.append(
        ("sources", sources)
    )

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

st.caption(
    "Built with FastAPI + RAG + Ollama + Streamlit"
)