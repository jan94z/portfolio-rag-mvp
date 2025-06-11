from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from typing import List
import os

COLLECTION_NAME = "docs"
VECTOR_SIZE = 384  # For all-MiniLM-L6-v2

client = QdrantClient(host="localhost", port=6333)  # Or 'qdrant' if Docker Compose
client = QdrantClient(host=os.environ.get("QDRANT_HOST", "localhost"),
                      port=int(os.environ.get("QDRANT_PORT", 6333)))

def ensure_collection():
    """Create or recreate the vector collection with the correct config."""
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )

def upsert_chunks(chunks: List[str], vectors: List[List[float]], doc_id: str = None):
    """
    Upsert chunks and their embeddings to Qdrant.

    Args:
        chunks (List[str]): List of text chunks.
        vectors (List[List[float]]): List of embedding vectors.
        doc_id (str): Optional document identifier for source tracking.
    """
    ensure_collection()
    points = [
        PointStruct(
            id=idx,  # Let Qdrant autogenerate
            vector=vector,
            payload={"text": chunk, "doc_id": doc_id} if doc_id else {"text": chunk}
        )
        for idx, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def semantic_search(query_vector: List[float], top_k: int = 5) -> List[dict]:
    """
    Search the collection for the top_k most similar vectors.

    Args:
        query_vector (List[float]): The query embedding.
        top_k (int): Number of results.

    Returns:
        List[dict]: List of dicts with 'text' and 'score'.
    """
    ensure_collection()
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
        with_vectors=False,
    )
    return [
        {"text": hit.payload.get("text", ""), "score": hit.score, "doc_id": hit.payload.get("doc_id", None)}
        for hit in results
    ]
