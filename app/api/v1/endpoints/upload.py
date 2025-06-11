# TODO
# THIS MAY BE RELEVANT LATER BUT IS NOT NEEDED NOW

# from fastapi import APIRouter, UploadFile, File, HTTPException
# from app.core import pdf_utils, chunking, embedding, qdrant_client

# router = APIRouter()

# @router.post("/upload")
# async def upload_pdf(file: UploadFile = File(...)):
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only PDF files supported.")

#     # 1. Extract text from PDF
#     text = pdf_utils.extract_text(await file.read())

#     # 2. Chunk the text
#     chunks = chunking.chunk_text(text)

#     # 3. Generate embeddings
#     vectors = embedding.embed_chunks(chunks)

#     # 4. Upsert into Qdrant
#     qdrant_client.upsert_chunks(chunks, vectors)

#     return {"message": "Document processed and indexed", "chunks": len(chunks)}
