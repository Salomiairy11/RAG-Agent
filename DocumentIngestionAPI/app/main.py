import uuid
from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.text_extraction import extract_text, UnsupportedFileType, EmptyOrUnreadableFile
from app.services.chunking import get_text_chunks
from langchain_huggingface import HuggingFaceEmbeddings

from app.db.models import SessionLocal
from app.db import crud
from app.services.vectorstore import ensure_index_and_upsert

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
    try:
        content_bytes = await file.read()
        file_type = file.content_type
        filename = file.filename

        content = extract_text(file_type, content_bytes)
        
        docs_to_index, stats = get_text_chunks(strategy, filename, content, embeddings)

        if not docs_to_index:
            raise HTTPException(status_code=400, detail="No chunks produced from the file.")

        document_id = str(uuid.uuid4())
        
        pinecone_mapping = ensure_index_and_upsert(docs_to_index, embeddings, document_id=document_id)

        metadata_rows = []
        for doc in docs_to_index:
            meta = doc.metadata or {}
            chunk_index = meta.get("chunk_index")
            chunk_strategy = meta.get("strategy")
            metadata = {
                "document_id": document_id,
                "chunk_index": chunk_index,
                "chunk_strategy": chunk_strategy,
                "chunk_filename": filename,
                "pinecone_id": pinecone_mapping.get((chunk_strategy, chunk_index)),  # depends on how vectorstore returns ids
                "extra": {"text_preview": doc.page_content[:200]},
            }
            row = crud.insert_chunk_metadata(db, metadata)
            metadata_rows.append({
                "id": row.id,
                "chunk_index": row.chunk_index,
                "pinecone_id": row.pinecone_id,
            })

        response = {
            "document_id": document_id,
            "stats": stats,
            "indexed_chunks": len(metadata_rows),
        }
        return response

    except UnsupportedFileType as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EmptyOrUnreadableFile as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        # log in real app
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
        
    
    
    
    