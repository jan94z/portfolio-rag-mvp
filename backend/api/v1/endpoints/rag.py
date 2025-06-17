from fastapi import APIRouter, HTTPException, Depends
from backend.core.embedding import embed_chunks
from backend.core.qdrant_client import semantic_search
from backend.core.auth import get_current_user
from openai import OpenAI
import os
from pydantic import BaseModel
from backend.core.sql import SessionLocal, get_user_by_username, increment_prompt_count, log_prompt
from backend.main import limiter
import yaml

with open("system_prompt.yaml", "r") as f:
    config = yaml.safe_load(f)

instructions = config["system_prompt"]

router = APIRouter()

# --- MODEL ---
class RagRequest(BaseModel):
    query: str
    top_k: int = 5
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 128
    temperature: float = 0.3

# --- ENDPOINT ---
@router.post("/rag")
@limiter.limit("10/minute")
def rag_query(
    rag_request: RagRequest,
    username: str = (Depends(get_current_user))
):
    db = SessionLocal()
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    # Enforce prompt limit
    if user.prompt_count >= user.prompt_limit:
        raise HTTPException(status_code=403, detail="Prompt limit reached.")
    # Increment count and save prompt (must be atomic in production, for now it's fine)
    if not increment_prompt_count(db, username):
        raise HTTPException(status_code=403, detail="Prompt limit reached.")

    """
    RAG: retrieve relevant chunks and generate answer via OpenAI.
    """
    # 1. Retrieve relevant context
    query_vector = embed_chunks([rag_request.query])[0]
    retrieved = semantic_search(query_vector, top_k=rag_request.top_k)

    context = "\n---\n".join([chunk["text"] for chunk in retrieved])
    prompt = (
        f"Use the following context to answer the user's question.'"
        f"Context:\n{context}\n\n"
        f"Question: {rag_request.query}\n"
        f"Answer:"
    )

    # 2. Call OpenAI LLM (ChatCompletion API)
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model=rag_request.model,
            messages=[
                {"role": "system", "content":  instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=rag_request.temperature,
            max_tokens=rag_request.max_tokens
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {e}")

    answer = response.choices[0].message.content.strip()

    # return {
    #     "answer": answer,
    #     "references": [c["text"] for c in retrieved],
    #     "raw_chunks": retrieved
    # }

    log_prompt(db, username, rag_request.query, answer)
    return {
        "answer": answer,
        "prompt_count": user.prompt_count,
        "prompt_limit": user.prompt_limit
    }
