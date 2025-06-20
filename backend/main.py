from fastapi import FastAPI
from backend.api.v1.endpoints import search, rag, auth
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from backend.core.rate_limit import limiter


app = FastAPI(
    title="RAG Backend Portfolio",
    version="0.1.0"
)


app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "You have hit the prompt limit. Please wait before trying again."},
    )


app.include_router(auth.router, prefix="/api/v1")
# app.include_router(search.router, prefix="/api/v1")
app.include_router(rag.router, prefix="/api/v1")
