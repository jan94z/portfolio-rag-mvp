import os
from pathlib import Path
import click
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv

from app.core.doc_parsing import parse_txt_file
from app.core.chunking import chunk_text
from app.core.embedding import embed_chunks

load_dotenv("/home/jan/portfolio-rag-mvp/.env")
VECTOR_SIZE = 384  # For all-MiniLM-L6-v2
COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION")
client = QdrantClient(host=os.environ.get("QDRANT_HOST", "qdrant"),
                      port=int(os.environ.get("QDRANT_PORT", 6333)))

def ensure_collection():
    """Create or recreate the vector collection with the correct config."""

    if not client.collection_exists(collection_name=COLLECTION_NAME):
        print(f"Collection '{COLLECTION_NAME}' does not exist. Creating it...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")

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

def ingest_txt_file(filepath: str, doc_id: str = None):
    print(f"Ingesting {filepath} ...")
    # 1. Parse TXT file
    text = parse_txt_file(filepath)
    # # 2. Chunk text
    chunks = chunk_text(text)
    print(f"Chunked into {len(chunks)} pieces.")
    # # 3. Embed chunks
    vectors = embed_chunks(chunks)
    # # 4. Upsert to Qdrant
    upsert_chunks(chunks, vectors, doc_id=doc_id)
    print(f"Inserted {len(chunks)} chunks to Qdrant.")

@click.command()
@click.option("--folderpath", "-fp", prompt="Folder path containing TXT files", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def main(folderpath: str):
    folderpath = Path(folderpath)
    for idx, file in enumerate(os.listdir(folderpath)):
        if file.endswith(".txt"):
            ingest_txt_file(folderpath / file, doc_id=idx)
        else:
            print(f"Skipping non-TXT file: {file}")

if __name__ == "__main__":
    main()