from fastapi import APIRouter, Query
from backend.core.embedding import embed_chunks
from backend.core.qdrant_client import semantic_search
from pydantic import BaseModel
from slowapi.decorator import limiter


router = APIRouter()

# --- MODEL ---
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

# --- ENDPOINT ---
@router.get("/search")
@limiter.limit("10/minute")
def search(search_request: SearchRequest):
    """
    Semantic search: return top-k relevant chunks.
    """
    query_vector = embed_chunks([search_request.query])[0]
    results = semantic_search(query_vector, top_k=search_request.top_k)
    return {"results": results}
