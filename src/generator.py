from langchain_community.chat_models import ChatOllama

def generate_answer(query, docs):
    llm = ChatOllama(model="llama3")

    context = "\n\n".join([doc.page_content for doc in docs])

    # Remove duplicate sources
    sources = list(set([
        f"{doc.metadata.get('source')} (Page {doc.metadata.get('page', 'N/A')})"
        for doc in docs
    ]))

    sources_text = "\n".join(sources)

    prompt = f"""
You are a helpful assistant.

Answer using ONLY the context below.

Rules:
- If exact answer is not present but can be inferred, explain using context
- If completely missing, say "I don't know"
- Format the answer in clean bullet points
- Always use "-" for bullet points
- Keep answers clear and structured (3–6 points)

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    return response.content.strip(), sources_text