import os

from langchain_community.chat_models import ChatOllama


def generate_answer(query, docs):

    llm = ChatOllama(

        model=os.getenv(
            "MODEL_NAME",
            "phi3"
        ),

        base_url=os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434"
        )
    )

    # -----------------------------
    # Combine Retrieved Context
    # -----------------------------
    context = "\n\n".join([

        doc.page_content

        for doc in docs

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
You are a strict document question-answering assistant.

You MUST answer ONLY from the provided context.

Rules:
- If the answer is NOT clearly present in the context,
  respond ONLY with:
  "I don't know based on the provided documents."

- Do NOT use outside knowledge.
- Do NOT make assumptions.
- Do NOT hallucinate.
- Keep answers concise.
- Use bullet points when appropriate.

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    return response.content.strip(), sources_text