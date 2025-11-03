from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.text_extraction import extract_text
from app.services.chunking import get_text_chunks
from langchain_huggingface import HuggingFaceEmbeddings
from datetime import datetime
import uuid

from app.db.models import SessionLocal
from app.db import crud
from app.services.vectorstore import store_embeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/uploadfile/")
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

    content = extract_text(file_type, content_bytes)
    
    docs_to_index, stats = get_text_chunks(strategy, filename, content, embeddings)

    if not docs_to_index:
        raise HTTPException(status_code=400, detail="No chunks produced from the file.")

    # Store embeddings (side-effect)
    store_embeddings(docs_to_index)

    # Build metadata list from produced documents and use the injected DB session
    metadata_list = []
    document_id = str(uuid.uuid4())
    for doc in docs_to_index:
        metadata_list.append(
            {
                "document_id": document_id,
                "chunk_index": doc.metadata.get("chunk_index"),
                "chunk_strategy": doc.metadata.get("strategy"),
                "chunk_filename": filename,
                "created_at": datetime.utcnow(),
            }
        )

    crud.insert_chunks(db, metadata_list)

    return {"message": "File uploaded, chunks stored, and metadata saved.", "chunks": len(docs_to_index)}