from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document

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

    # Save the uploaded file to the specified path
    with file_path.open("wb") as buffer:
        while chunk := file.file.read(1024 * 1024):  # Read in 1MB chunks
            buffer.write(chunk)

    # Get file size
    file_size = file_path.stat().st_size

    # Create a new Document instance
    document = Document(
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=str(file_path),
        content_type=file.content_type,
        file_size=file_size,
        user_id=user_id,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document
