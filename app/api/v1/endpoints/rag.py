from fastapi import APIRouter, Query, HTTPException
from app.core.embedding import embed_chunks
from app.core.qdrant_client import semantic_search
from openai import OpenAI
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()  # Load environment variables from .env file

# Make sure your OpenAI API key is set as an environment variable: OPENAI_API_KEY

@router.post("/rag")
def rag_query(
    query: str = Query(..., description="User question"),
    top_k: int = 5,
    model: str = "gpt-3.5-turbo"
):
    """
    RAG: retrieve relevant chunks and generate answer via OpenAI.
    """
    # 1. Retrieve relevant context
    query_vector = embed_chunks([query])[0]
    retrieved = semantic_search(query_vector, top_k=top_k)

    context = "\n---\n".join([chunk["text"] for chunk in retrieved])
    prompt = (
        f"Use the following context to answer the user's question.\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )

    # 2. Call OpenAI LLM (ChatCompletion API)
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an assistant that provides answers about Jan using the given context."},
                {"role": "developer", "content": "You should be funny and creative in your responses. Stick to the truth but feel free to add some humor. Speak like "
                "a 20 year old douchebag who is super interested in AI and coding."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=256
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {e}")

    answer = response.choices[0].message.content.strip()

    return {
        "answer": answer,
        "references": [c["text"] for c in retrieved],
        "raw_chunks": retrieved
    }


