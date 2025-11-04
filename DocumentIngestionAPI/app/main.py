from fastapi import APIRouter, UploadFile, File, Query, Depends
from sqlalchemy.orm import Session

from .db.models import SessionLocal
from .services.upload import upload_to_db

router = APIRouter()

def get_db():
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
):
    """
    Upload a text or PDF file, extract content, and apply the selected chunking strategy.
    """
    
    content_bytes = await file.read()
    file_type = file.content_type
    filename = file.filename
    result = upload_to_db(content_bytes, file_type, filename, strategy, db)
    return {
        "message": "File uploaded, chunks stored, and metadata saved.",
        **result
    }
