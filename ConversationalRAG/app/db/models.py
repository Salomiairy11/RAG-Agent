from sqlalchemy import Column, Integer, String, Date, Time, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, sessionmaker
from ..config import get_engine

engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    date = Column(Date)
    time = Column(Time)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

Base.metadata.create_all(bind=engine)
