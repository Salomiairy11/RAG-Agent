import logging
from datetime import date, time
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    TIMESTAMP,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from ..config import get_engine

# logger
logger = logging.getLogger(__name__)

# Database setup
engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Interview(Base):
    """Database model for storing interview booking details."""
    
    __tablename__ = "interviews"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)
    email: str = Column(String(120), nullable=False)
    date: date = Column(Date, nullable=False)
    time: time = Column(Time, nullable=False)
    created_at = Column(
        TIMESTAMP, 
        nullable=False, 
        server_default=text("CURRENT_TIMESTAMP")
    )
    
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Interview table created or already exists.")
except Exception as e:
    logger.error("Error while creating tables: %s", str(e), exc_info=True)
