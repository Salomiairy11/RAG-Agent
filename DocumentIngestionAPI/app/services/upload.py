from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict

from .text_extraction import extract_text
from .chunking import get_text_chunks
from .build_metadata import build_metadata

from ..db.crud import insert_chunks
from .vectorstore import store_embeddings
from ..config import get_embeddings

def upload_to_db(content_bytes: bytes,
    file_type: str,
    filename: str,
    strategy: str,
    db: Session
) -> Dict[str, Any]:
    """
    Process a file: extract text, chunk it, store embeddings, and save metadata to the database.

    Args:
        content_bytes (bytes): Raw file content.
        file_type (str): MIME type of the file ('text/plain' or 'application/pdf').
        filename (str): Name of the uploaded file.
        strategy (str): Chunking strategy ('recursive' or 'semantic').
        db (Session): SQLAlchemy database session to insert metadata.

    Returns:
        Dict[str, Any]: Dictionary containing the total number of chunks and the first few chunk previews.

    Raises:
        HTTPException: If no chunks are produced from the file.
    """

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

