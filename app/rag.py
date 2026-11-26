from app.config import settings
from app.llm import generate
from app.vector_store import search

RAG_SYSTEM_PROMPT = """You are ResolveAgent, a support assistant for Razorpay merchants and their customers.

Rules:
1. Answer ONLY using the information in the provided context.
2. If the context does not contain the answer, reply exactly: "I don't have information on that in the Razorpay docs." Do not guess.
3. Cite the sources you used with their numbers, like [1] or [2].
4. Keep answers short and clear: 3 to 6 sentences, or short numbered steps for how-to questions.
5. Never invent numbers, timelines, fees, or API fields that are not in the context."""

NO_ANSWER = "I don't have information on that in the Razorpay docs."


def build_prompt(question: str, hits: list[dict]) -> str:
    blocks = [
        f"[{i}] {hit['title']}\nSource: {hit['url']}\n{hit['text']}"
        for i, hit in enumerate(hits, start=1)
    ]
    context = "\n\n---\n\n".join(blocks)
    return f"Context:\n{context}\n\nQuestion: {question}"


def answer_question(question: str) -> dict:
    hits = search(
        question,
        limit=settings.top_k,
        name=settings.docs_collection,
        score_threshold=settings.score_threshold,
    )

    if not hits:
        return {"answer": NO_ANSWER, "sources": [], "input_tokens": 0, "output_tokens": 0}

    result = generate(build_prompt(question, hits), system_prompt=RAG_SYSTEM_PROMPT)
    sources = [
        {"title": hit["title"], "url": hit["url"], "score": round(hit["score"], 3)}
        for hit in hits
    ]
    return {**result, "sources": sources}