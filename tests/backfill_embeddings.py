import app.db.models

from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding

def backfill_embeddings():
    db = SessionLocal()


    try:
        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.embedding.is_(None))
            .order_by(DocumentChunk.document_id, DocumentChunk.chunk_index)
        )

        chunks = db.scalars(statement).all()

        if not chunks:
            print("All chunks already have embeddings.")
            return
        
        print(f"Generating embeddings for {len(chunks)} chunks...")

        for index, chunk in enumerate(chunks, start=1):
            chunk.embedding = generate_embedding(chunk.content)

            if index % 10 == 0 or index == len(chunks):
                print(f"Processed {index}/{len(chunks)} chunks")

        db.commit()
        print("Embedding backfill completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

if __name__ == "__main__":
    backfill_embeddings()