from pathlib import Path

def parse_txt_file(filepath: str) -> str:
    """
    Reads the entire content of a .txt file as a string.

    Args:
        filepath (str): Path to the txt file.

    Returns:
        str: File content.
    """
    path = Path(filepath)
    if not path.exists() or not path.suffix == ".txt":
        raise ValueError(f"File {filepath} does not exist or is not a .txt file.")
    with path.open("r", encoding="utf-8") as f:
        return f.read()
