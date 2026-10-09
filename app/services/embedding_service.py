from fastembed import TextEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"

_embedding_model = None

def get_embedding_model() -> TextEmbedding:
    """Load the embedding model once and reuse it."""
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = TextEmbedding(model_name=MODEL_NAME)

    return _embedding_model

def generate_embedding(text: str) -> list[float]:
    """Generate a 384-dimensional embedding for a text chunk."""
    if not text.strip():
        raise ValueError("Cannot generate an embedding for empty text.")
    
    model = get_embedding_model()
    embedding = next(model.embed([text]))

    return embedding.tolist()