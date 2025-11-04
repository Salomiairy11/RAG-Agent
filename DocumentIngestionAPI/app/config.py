import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy import create_engine

load_dotenv()

def get_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

def get_index_name():
    INDEX_NAME = os.getenv("INDEX_NAME")
    if not INDEX_NAME:
        raise ValueError("INDEX NAME environment variable not set.")
    return  INDEX_NAME

# Pinecone setup
def get_pineconeClient():
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE API KEY environment variable not set.")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc


#database setup
def get_engine():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return engine



