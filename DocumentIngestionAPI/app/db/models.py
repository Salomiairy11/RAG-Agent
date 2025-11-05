from datetime import datetime
from ..config import get_engine
from typing import Any

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,   
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# logger
logger = logging.getLogger(__name__)

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChunkMetadata(Base):
    """SQLAlchemy model for storing metadata of text chunks."""

    __tablename__ = "chunk_metadata"

    id: Any = Column(Integer, primary_key=True, autoincrement=True)
    chunk_index: int = Column(Integer, nullable=False)
    chunk_strategy: str = Column(String, nullable=False)
    chunk_filename: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now, nullable=False)
    

Base.metadata.create_all(bind=engine)
logger.info("Chunk MetaData table created or already exists.")
  


