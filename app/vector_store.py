import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import settings
from app.embeddings import EMBEDDING_DIM, embed_documents, embed_query

qdrant = QdrantClient(url=settings.qdrant_url)
COLLECTION = "playground"


def ensure_collection(name: str = COLLECTION) -> None:
    if not qdrant.collection_exists(name):
        qdrant.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


def add_texts(texts: list[str], name: str = COLLECTION) -> None:
    vectors = embed_documents(texts)
    points = [
        PointStruct(
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, text)),
            vector=vector,
            payload={"text": text},
        )
        for text, vector in zip(texts, vectors)
    ]
    qdrant.upsert(collection_name=name, points=points)


def search(query: str, limit: int = 3, name: str = COLLECTION) -> list[dict]:
    hits = qdrant.query_points(
        collection_name=name,
        query=embed_query(query),
        limit=limit,
    ).points
    return [{"score": hit.score, "text": hit.payload["text"]} for hit in hits]