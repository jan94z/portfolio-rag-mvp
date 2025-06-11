from fastapi import FastAPI
from app.api.v1.endpoints import search, rag

app = FastAPI(
    title="RAG Backend Portfolio",
    version="0.1.0"
)

app.include_router(search.router, prefix="/api/v1")
app.include_router(rag.router, prefix="/api/v1")
