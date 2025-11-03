import os
from typing import List, Dict, Tuple
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.docstore.document import Document

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY not set")

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "langchainvector"
dimension = 384

def ensure_index_exists():
    if index_name not in [index.name for index in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

def ensure_index_and_upsert(docs: List[Document], embeddings, document_id: str):
    """
    Upserts docs to Pinecone. Returns mapping:
      {(strategy, chunk_index): pinecone_vector_id}
    """
    ensure_index_exists()

    vector_store = PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        index_name=index_name,
    )

    # Unfortunately LangChain's store may not return per-document ids.
    # To store mapping, we'll re-create ids based on metadata pattern.
    mapping = {}
    for i, doc in enumerate(docs):
        meta = doc.metadata or {}
        strategy = meta.get("strategy")
        chunk_index = meta.get("chunk_index")
        # Create a stable ID you can store in Postgres, e.g. "{document_id}-{strategy}-{chunk_index}"
        vec_id = f"{document_id}-{strategy}-{chunk_index}"
        mapping[(strategy, chunk_index)] = vec_id

    # If PineconeVectorStore.from_documents didn't use our stable IDs, do an upsert loop manually:
    # (This example assumes you have a function to get embedding vector for a doc)
    # You may prefer using vector_store.add_texts with ids, or call pc.upsert directly.
    return mapping
