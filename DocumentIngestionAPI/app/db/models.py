import os
from datetime import datetime
from dotenv import load_dotenv

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,   
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment")

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChunkMetadata(Base):
    __tablename__ = "chunk_metadata"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_strategy = Column(String, nullable=False)
    chunk_filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
Base.metadata.create_all(bind=engine)

