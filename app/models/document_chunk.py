from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column( Integer, primary_key=True, index=True, )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    chunk_index: Mapped[int] = mapped_column( Integer, nullable=False,)

    content: Mapped[str] = mapped_column(Text, nullable=False,)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    document = relationship("Document", back_populates="chunks")

    embedding = mapped_column(Vector(384), nullable=True)