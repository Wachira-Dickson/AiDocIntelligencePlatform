def chunk_text(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 150,
) -> list[str]:
    
    """
    Args:
        text: Extracted document text.
        chunk_size: Maximum approximate characters per chunk.
        overlap: Approximate characters shared between chunks.
        
        Returns:
        A list of text chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size"
        )
    
    text = text.strip()

    if not text:
        return []
    
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        #Prefer ending at a word boundary.
        if end < len(text):
            boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        # Move backwards slightly so adjacent chunks share context
        start = max(end - overlap, start + 1)
    
    return chunks