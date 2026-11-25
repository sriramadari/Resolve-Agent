from google.genai import types

from app.config import settings
from app.gemini_client import client

EMBEDDING_DIM = 768


def _embed(texts: list[str]) -> list[list[float]]:
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    result = client.models.embed_content(
        model=settings.embedding_model,
        contents=contents,
        config=types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIM),
    )
    vectors = [e.values for e in result.embeddings]
    assert len(vectors) == len(texts), "Expected one embedding per text"
    return vectors


def embed_query(question: str) -> list[float]:
    return _embed([f"task: question answering | query: {question}"])[0]


def embed_documents(texts: list[str], title: str = "none") -> list[list[float]]:
    return _embed([f"title: {title} | text: {t}" for t in texts])