import re

def clean_manuscript_text(text: str) -> str:
    """
    Removes excessive whitespaces, broken markdown symbols, and 
    standardizes line breaks for clean agent consumption.
    """
    if not text:
        return ""
    # Normalize whitespaces and remove hidden control characters
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    """
    Splits long drafts or reference papers into smaller semantic windows 
    so they fit safely inside the LLM and Vector Database context limits.
    """
    cleaned = clean_manuscript_text(text)
    words = cleaned.split(" ")
    chunks = []
    current_chunk = []
    current_count = 0

    for word in words:
        current_chunk.append(word)
        current_count += 1
        if current_count >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_count = 0
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks
