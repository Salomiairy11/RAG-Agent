from typing import List

from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from ..config import get_index_name, get_pineconeClient, get_embeddings

# Initialize Pinecone client, embeddings, and index name
pc = get_pineconeClient()
embeddings = get_embeddings()
INDEX_NAME = get_index_name()

def store_embeddings(docs: List[Document]) -> PineconeVectorStore:
    """
    Store embeddings for a list of documents in Pinecone.

    Args:
        docs (List[Document]): List of LangChain Document objects to embed.

    Returns:
        PineconeVectorStore: Vector store containing the stored embeddings.
    """
    if INDEX_NAME not in [index.name for index in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        index_name=INDEX_NAME
    )

def get_vector_store()-> PineconeVectorStore:
    """
    Retrieve a PineconeVectorStore connected to the existing index.

    Returns:
        PineconeVectorStore: Vector store instance for querying.
    """
    vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    return vectorstore
