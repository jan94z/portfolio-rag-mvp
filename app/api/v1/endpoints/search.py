from fastapi import APIRouter, Query
from app.core.embedding import embed_chunks
from app.core.qdrant_client import semantic_search

router = APIRouter()

@router.get("/search")
def search(query: str = Query(..., description="User query string"), top_k: int = 5):
    """
    Semantic search: return top-k relevant chunks.
    """
    query_vector = embed_chunks([query])[0]
    results = semantic_search(query_vector, top_k=top_k)
    return {"results": results}
