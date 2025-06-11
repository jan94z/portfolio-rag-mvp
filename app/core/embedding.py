from sentence_transformers import SentenceTransformer
from typing import List
import torch

# Load model once at import. Reuse for all requests.
# all-MiniLM-L6-v2 is a good CPU-friendly default for RAG.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

try:
    model = SentenceTransformer(MODEL_NAME)
except Exception as e:
    raise RuntimeError(f"Could not load embedding model '{MODEL_NAME}': {e}")

def embed_chunks(chunks: List[str]) -> List[list]:
    """
    Takes a list of text chunks and returns a list of embedding vectors.
    
    Args:
        chunks (List[str]): List of text chunks.
        
    Returns:
        List[list]: List of embedding vectors (as lists of floats).
    """
    if not chunks:
        return []
    # Returns a list of numpy arrays; convert to list for serialization if needed
    embeddings = model.encode(chunks, show_progress_bar=False, normalize_embeddings=True)
    # .tolist() converts numpy arrays to lists, good for JSON/db
    return embeddings.tolist()

# This is a simple script to check if the model is loaded correctly and on which device.
if __name__ == "__main__":
    # Check if torch CUDA is available
    flag = torch.cuda.is_available()
    print("Torch CUDA available:", flag)

    if flag:
        try:
            # Get the first parameter of the transformer and check its device
            device = next(model[0].parameters()).device
        except Exception:
            device = "Unknown"

        print(f"SentenceTransformer model loaded on device: {device}")

