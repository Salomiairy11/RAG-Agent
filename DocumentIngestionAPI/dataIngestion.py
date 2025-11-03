from fastapi import FastAPI, UploadFile, File, Query
import fitz  
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain_pinecone import PineconeVectorStore

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
pinecone_key = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=pinecone_key)

def recursive_text_splitter(content: str):
    """Splits text using LangChain's RecursiveCharacterTextSplitter."""
    recursive_char_chunker = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ".", "?", "!"],
        chunk_size=300,
        chunk_overlap=0,
        length_function=len,
    )
    return recursive_char_chunker.split_text(content)

def semantic_text_splitter(content: str):
    """Splits text using LangChain's SemanticChunker (HuggingFace Embeddings)."""
    semantic_chunker = SemanticChunker(embeddings)
    return semantic_chunker.split_text(content)

def retrieve_query(vector_store,query, k=2):
    matching_results = vector_store.similarity_search(query, k=k)
    return matching_results


app = FastAPI()
@app.post("/uploadfile/")
async def upload_file(
    file: UploadFile = File(...),
    strategy: str = Query("both", description="Choose 'recursive', 'semantic', or 'both'")
):
    """
    Upload a text or PDF file, extract content, and apply the selected chunking strategy.
    """
    
    content_bytes = await file.read()
    docs_to_index = []
    content = ""
    
    #handling file reading based on content type
    if file.content_type == 'text/plain':
        content = content_bytes.decode('utf-8')
    elif file.content_type == 'application/pdf':
        try:
            with fitz.open(stream=content_bytes, filetype="pdf") as doc:
                for page in doc:
                    content += page.get_text()
        except Exception as e:
            return {"error": f"Failed to read PDF: {e}"}
    else:
        return {"error": "Unsupported file type. Please upload .txt or .pdf"}
    
    if not content.strip():
        return {"error": "The file appears to be empty or unreadable."}
    
    #handling chunking of text
    result = {}
    if strategy in ["recursive", "both"]:
        recursive_chunks = recursive_text_splitter(content)
        result["recursive_chunk_count"] = len(recursive_chunks)
        result["Recursive Splitter Chunks"] = recursive_chunks
        docs_to_index += [
            Document(
                page_content=chunk, 
                    metadata=
                        {
                           "strategy": "recursive",
                            "filename": file.filename,
                            "chunk_index": i
                        }
                    ) 
            for i, chunk in enumerate(recursive_chunks)
            ]

    if strategy in ["semantic", "both"]:
        semantic_chunks = semantic_text_splitter(embeddings, content)
        result["semantic_chunk_count"] = len(semantic_chunks)
        result["Semantic Splitter Chunks"] = semantic_chunks
        docs_to_index += [
            Document(
                page_content=chunk, 
                metadata=
                    {
                        "strategy": "semantic",
                        "filename": file.filename,
                        "chunk_index": i
                    }
                ) 
            for i, chunk in enumerate(semantic_chunks)
            ]

    result["strategy_used"] = strategy
    
    index_name = "langchainvector"
    if index_name not in [index.name for index in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    vector_store = PineconeVectorStore.from_documents(
        docs_to_index,
        embeddings,
        index_name=index_name
    )

    return result
