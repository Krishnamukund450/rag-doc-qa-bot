import os

from langchain_community.chat_models import ChatOllama


def generate_answer(query, docs):

    llm = ChatOllama(
        model="phi3",
        base_url="http://ollama:11434"
    )

    # -----------------------------
    # Combine Retrieved Context
    # -----------------------------
    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    # -----------------------------
    # Normalize Sources
    # -----------------------------
    sources = sorted(list(set([

        os.path.basename(
            doc.metadata.get("source", "")
        )

        +

        (
            f" (Page {doc.metadata.get('page')})"
            if doc.metadata.get("page") is not None
            else ""
        )

        for doc in docs

    ])))

    sources_text = "\n".join(sources)

    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = f"""
You are a helpful assistant.

Answer using ONLY the context below.

Rules:
- If exact answer is not present but can be inferred, explain using context
- If completely missing, say "I don't know"
- Format the answer in clean bullet points
- Always use "-" for bullet points

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    return response.content.strip(), sources_text