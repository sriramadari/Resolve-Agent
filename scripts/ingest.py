import json
import time
from pathlib import Path

from app.config import settings
from app.embeddings import embed_documents
from app.ingestion import chunk_markdown
from app.vector_store import recreate_collection, upsert_chunks

DOCS = Path("data/raw/docs.jsonl")
BATCH_SIZE = 50


def main() -> None:
    docs = [json.loads(line) for line in DOCS.read_text(encoding="utf-8").splitlines()]

    chunks = []
    for doc in docs:
        for i, text in enumerate(chunk_markdown(doc["text"])):
            chunks.append({"url": doc["url"], "title": doc["title"], "chunk_index": i, "text": text})

    sizes = [len(c["text"]) for c in chunks]
    print(f"{len(docs)} pages -> {len(chunks)} chunks")
    print(f"Chunk sizes: min {min(sizes)}, avg {sum(sizes) // len(sizes)}, max {max(sizes)}")

    recreate_collection(settings.docs_collection)

    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start : start + BATCH_SIZE]
        vectors = embed_documents([c["text"] for c in batch], titles=[c["title"] for c in batch])
        upsert_chunks(batch, vectors, name=settings.docs_collection)
        print(f"Indexed {start + len(batch)}/{len(chunks)}")
        time.sleep(1)


if __name__ == "__main__":
    main()