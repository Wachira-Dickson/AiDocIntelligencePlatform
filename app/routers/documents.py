from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.models.user import User
from app.db.database import get_db
from app.services.document_service import (
    ALLOWED_CONTENT_TYPES,
    save_document,
)

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )
    
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed types are: {', '.join(ALLOWED_CONTENT_TYPES)}"
        )
    
    document = save_document(
        db=db,
        file=file,
        user_id=current_user.id,
    )

    return {
        "message": "Document uploaded successfully.",
        "document": {
            "id": document.id,
            "original_filename": document.original_filename,
            "stored_filename": document.stored_filename,
            "file_path": document.file_path,
            "content_type": document.content_type,
            "file_size": document.file_size,
            "uploaded_at": document.uploaded_at.isoformat(),
            "extracted_text": document.extracted_text,
        }, 
    }