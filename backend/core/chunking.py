from langchain_text_splitters import TokenTextSplitter
from langchain.text_splitter import SpacyTextSplitter
from typing import List

# token did not work well, because of my personal information data type...
# def chunk_text(
#     text: str, 
#     chunk_size: int = 400,     # tokens per chunk (common range: 300-512)
#     chunk_overlap: int = 80,   # tokens overlapped with previous chunk
#     encoding_name: str = "cl100k_base" # OpenAI models, or use "gpt2" for others
# ) -> List[str]:
#     """
#     Splits text into token-based chunks using LangChain's TokenTextSplitter.

#     Args:
#         text: The full document as a string.
#         chunk_size: Tokens per chunk.
#         chunk_overlap: Overlap tokens between chunks.
#         encoding_name: Tokenizer name for correct splitting.

#     Returns:
#         List of string chunks.
#     """
#     splitter = TokenTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         encoding_name=encoding_name
#     )
#     chunks = splitter.split_text(text)
#     return chunks

# now using sentence based chunking instead of token based chunking
def chunk_text(
    text: str, 
    chunk_size: int = 400,    
    chunk_overlap: int = 80, 
) -> List[str]:
    """
    Splits text into sentence-based chunks using LangChain's SpacyTextSplitter.

    Args:
        text: The full document as a string.
        chunk_size: Tokens per chunk.
        chunk_overlap: Overlap tokens between chunks.

    Returns:
        List of string chunks.
    """
    splitter = SpacyTextSplitter(
        separator=".", # Use period as sentence separator
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    return chunks