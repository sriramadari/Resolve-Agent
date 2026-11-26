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


def recreate_collection(name: str) -> None:
    if qdrant.collection_exists(name):
        qdrant.delete_collection(name)
    qdrant.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )


def upsert_chunks(chunks: list[dict], vectors: list[list[float]], name: str) -> None:
    points = [
        PointStruct(
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{chunk['url']}#{chunk['chunk_index']}")),
            vector=vector,
            payload=chunk,
        )
        for chunk, vector in zip(chunks, vectors)
    ]
    qdrant.upsert(collection_name=name, points=points)


def search(
    query: str,
    limit: int = 3,
    name: str = COLLECTION,
    score_threshold: float | None = None,
) -> list[dict]:
    hits = qdrant.query_points(
        collection_name=name,
        query=embed_query(query),
        limit=limit,
        score_threshold=score_threshold,
    ).points
    return [{"score": hit.score, **hit.payload} for hit in hits]