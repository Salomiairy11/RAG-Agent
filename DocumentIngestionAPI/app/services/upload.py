from fastapi import HTTPException
from sqlalchemy.orm import Session

from .text_extraction import extract_text
from .chunking import get_text_chunks
from .build_metadata import build_metadata

from ..db.crud import insert_chunks
from .vectorstore import store_embeddings
from ..config import get_embeddings

def upload_to_db(content_bytes, file_type, filename, strategy, db: Session):

    content = extract_text(file_type, content_bytes)
    embeddings = get_embeddings()
    
    docs_to_index, stats = get_text_chunks(strategy, filename, content, embeddings)

    if not docs_to_index:
        raise HTTPException(status_code=400, detail="No chunks produced from the file.")

    # Store embeddings
    store_embeddings(docs_to_index)

    # Build metadata list from produced documents and use the injected DB session
    metadata_list = build_metadata(docs_to_index, filename)

    insert_chunks(db, metadata_list)
    
    top_chunks_response = [
        {"chunk_id": doc.metadata.get("chunk_index"), "chunk_text": doc.page_content}
        for doc in docs_to_index[:5]
    ]

    return {"chunks_length": len(docs_to_index), "top_chunks": top_chunks_response}

