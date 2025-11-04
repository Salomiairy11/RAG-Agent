from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from .db.models import SessionLocal
from .services.upload import upload_to_db

router = APIRouter()

def get_db()-> Session:
    """Dependency to provide a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/uploadfile/")
async def upload_file(
    file: UploadFile = File(...), 
    strategy: str = Query("recursive", description="Choose 'recursive' or 'semantic' "),
    db: Session = Depends(get_db)
)-> Dict[str, Any]:
    """
    Upload a text or PDF file, extract content, split into chunks, 
    store embeddings in the vector store, and save metadata in the database.

    Args:
        file (UploadFile): File uploaded by the user (.txt or .pdf).
        strategy (str): Chunking strategy ('recursive' or 'semantic').
        db (Session): SQLAlchemy database session.

    Returns:
        Dict[str, Any]: Details of the processed chunks including the top 5 chunks.
    """
    try:
        content_bytes = await file.read()
        file_type = file.content_type
        filename = file.filename
        result = upload_to_db(content_bytes, file_type, filename, strategy, db)
        return {
            "message": "File uploaded, chunks stored, and metadata saved.",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {e}")
