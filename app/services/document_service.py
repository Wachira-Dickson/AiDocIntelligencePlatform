from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.chunking_service import chunk_text
from app.services.extraction_service import extract_text

UPLOAD_DIR = Path("uploads")

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

def save_document(
    db: Session,
    file: UploadFile,
    user_id: int,
) -> Document:
    
    # Make sure the upload directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    #Generate a unique filename for the stored file
    file_extension = Path(file.filename).suffix
    stored_filename = f"{uuid4()}{file_extension}"

    file_path = UPLOAD_DIR / stored_filename

    try: 
    # Save the uploaded file to the specified path
        with file_path.open("wb") as buffer:
            while chunk := file.file.read(1024 * 1024):  # Read in 1MB chunks
                buffer.write(chunk)

        # Get file size
        file_size = file_path.stat().st_size

        extracted_text = extract_text(
            str(file_path),
            file.content_type or "",
        )

        # Create a new Document instance
        document = Document(
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            content_type=file.content_type,
            file_size=file_size,
            user_id=user_id,
            extracted_text=extracted_text,
        )

        db.add(document)
        db.flush()

        #Split the extracted text and save each chunk
        chunks = chunk_text(
            extracted_text,
            chunk_size=1000,
            overlap=150,
        )

        for index, content in enumerate(chunks):
            db.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=content,
                )
            )
        db.commit()
        db.refresh(document)

        return document
    
    except Exception:
        db.rollback()
    
        #Remove the file if processing or the database transaction fails.
        file_path.unlink(missing_ok=True)
        raise
