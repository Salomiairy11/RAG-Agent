from sqlalchemy.orm import Session
from app.db.models import ChunkMetadata
from typing import List, Dict

def insert_chunks(db: Session, metadata_list: List[Dict]):
    """
    Insert multiple chunk metadata rows at once.
    """
    for meta in metadata_list:
        row = ChunkMetadata(
            document_id=meta["document_id"],
            chunk_index=meta["chunk_index"],
            chunk_strategy=meta["chunk_strategy"],
            chunk_filename=meta["chunk_filename"],
            created_at=meta["created_at"]
        )
        db.add(row)
    db.commit()

