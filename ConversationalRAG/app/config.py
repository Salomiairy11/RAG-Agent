import os
from dotenv import load_dotenv
import redis
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from sqlalchemy import create_engine

load_dotenv()

# Redis setup
def get_redis_client():
    REDIS_URL = os.getenv("REDIS_URL")
    if not REDIS_URL:
        raise ValueError("REDIS_URL environment variable not set.")
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Pinecone setup
def get_vectorstore():
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    INDEX_NAME = "langchainvector"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    return vectorstore


#database setup
def get_engine():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return engine

# Google API
def get_google_api_key():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    return GOOGLE_API_KEY

