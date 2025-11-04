from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from ..config import get_index_name, get_pineconeClient, get_embeddings


pc = get_pineconeClient()
embeddings = get_embeddings()
INDEX_NAME = get_index_name()

def store_embeddings(docs):
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

def get_vector_store():
    vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    return vectorstore
