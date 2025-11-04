from datetime import datetime
from ..config import get_engine

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,   
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChunkMetadata(Base):
    __tablename__ = "chunk_metadata"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_index = Column(Integer, nullable=False)
    chunk_strategy = Column(String, nullable=False)
    chunk_filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
Base.metadata.create_all(bind=engine)

