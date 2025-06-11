import os
from pathlib import Path
import click

from app.core.doc_parsing import parse_txt_file
from app.core.chunking import chunk_text
from app.core.embedding import embed_chunks
from app.core.qdrant_client import upsert_chunks

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
