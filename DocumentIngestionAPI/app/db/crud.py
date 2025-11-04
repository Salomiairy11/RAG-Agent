from sqlalchemy.orm import Session
from .models import ChunkMetadata
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def insert_chunks(db: Session, metadata_list: List[Dict[str, any]])-> None:
    """
    Insert multiple chunk metadata rows at once.

    Args:
        db (Session): SQLAlchemy database session.
        metadata_list (List[Dict[str, any]]): List of metadata dicts for chunks.
    """
    try:
        for meta in metadata_list:
            row = ChunkMetadata(
                chunk_index=meta["chunk_index"],
                chunk_strategy=meta["chunk_strategy"],
                chunk_filename=meta["chunk_filename"],
                created_at=meta["created_at"]
            )
            db.add(row)
        db.commit()
        logger.info(f"Inserted {len(metadata_list)} chunk metadata rows successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to insert chunk metadata: {e}")
        raise


