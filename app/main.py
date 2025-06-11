from fastapi import FastAPI
from api.v1.endpoints import upload, search, rag

app = FastAPI(
    title="RAG Backend Portfolio",
    version="0.1.0"
)

# app.include_router(upload.router, prefix="/api/v1")
# app.include_router(search.router, prefix="/api/v1")
# app.include_router(rag.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Backend Portfolio API!"}