from qdrant_client import QdrantClient
from typing import List
import os

COLLECTION_NAME = "docs"
VECTOR_SIZE = 384  # For all-MiniLM-L6-v2

client = QdrantClient(host=os.environ.get("QDRANT_HOST", "localhost"),
                      port=int(os.environ.get("QDRANT_PORT", 6333)))

def semantic_search(query_vector: List[float], top_k: int = 5) -> List[dict]:
    """
    Search the collection for the top_k most similar vectors.

    Args:
        query_vector (List[float]): The query embedding.
        top_k (int): Number of results.

    Returns:
        List[dict]: List of dicts with 'text' and 'score'.
    """
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"Collection '{COLLECTION_NAME}' not found. Ensure it exists or recreate it.")
        raise e
    
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