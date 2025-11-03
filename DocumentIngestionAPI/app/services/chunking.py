from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.docstore.document import Document
from typing import List, Dict, Any

def recursive_text_splitter(content: str):
    """
    Splits text using LangChain's RecursiveCharacterTextSplitter.
    Returns:
      List of text chunks (List[str]).
    """
    recursive_char_chunker = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ".", "?", "!"],
        chunk_size=300,
        chunk_overlap=0,
        length_function=len,
    )
    return recursive_char_chunker.split_text(content)

def semantic_text_splitter(embeddings, content: str):
    """
    Splits text using LangChain's SemanticChunker (HuggingFace Embeddings).
    Returns:
      List of text chunks (List[str]).
    """
    semantic_chunker = SemanticChunker(embeddings)
    return semantic_chunker.split_text(content)


def get_text_chunks(strategy: str, filename, content: str, embeddings):
    """
    Get text chunks based on the specified strategy.
    Returns a tuple of (list of Document chunks, stats dictionary for metadata).
    
    """
    stats: Dict[str, Any] = {}
    docs_to_index: List[Document] = []

    if strategy == "recursive":
        recursive_chunks = recursive_text_splitter(content)
        stats["recursive_chunk_count"] = len(recursive_chunks)
        docs_to_index.extend(
            Document(
                page_content=chunk,
                metadata={
                    "strategy": "recursive",
                    "filename": filename,
                    "chunk_index": i,
                },
            )
            for i, chunk in enumerate(recursive_chunks)
        )

    if strategy == "semantic":
        semantic_chunks = semantic_text_splitter(embeddings, content)
        stats["semantic_chunk_count"] = len(semantic_chunks)
        docs_to_index.extend(
            Document(
                page_content=chunk,
                metadata={
                    "strategy": "semantic",
                    "filename": filename,
                    "chunk_index": i,
                },
            )
            for i, chunk in enumerate(semantic_chunks)
        )

    stats["strategy_used"] = strategy
    stats["total_chunks"] = len(docs_to_index)
    return docs_to_index, stats