from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from typing import List, Dict, Any, Tuple

def recursive_text_splitter(content: str)-> List[str]:
    """
    Split text using LangChain's RecursiveCharacterTextSplitter.

    Args:
        content (str): The text to split.

    Returns:
        List[str]: List of text chunks.
    """
    recursive_char_chunker = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ".", "?", "!"],
        chunk_size=300,
        chunk_overlap=0,
        length_function=len,
    )
    return recursive_char_chunker.split_text(content)

def semantic_text_splitter(embeddings, content: str)-> List[str]:
    """
    Split text using LangChain's SemanticChunker.

    Args:
        embeddings: HuggingFace embeddings object.
        content (str): The text to split.

    Returns:
        List[str]: List of text chunks.
    """
    semantic_chunker = SemanticChunker(embeddings)
    return semantic_chunker.split_text(content)


def get_text_chunks(
    strategy: str, filename: str, content: str, embeddings: Any) -> Tuple[List[Document], Dict[str, Any]]:
    """
    Generate text chunks based on the specified strategy.

    Args:
        strategy (str): 'recursive' or 'semantic'.
        filename (str): Name of the file being processed.
        content (str): Text content to chunk.
        embeddings: HuggingFace embeddings object (for semantic strategy).

    Returns:
        Tuple[List[Document], Dict[str, Any]]:
            - List of Document chunks with metadata.
            - Stats dictionary for chunking metadata.
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

    elif strategy == "semantic":
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
    
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")

    stats["strategy_used"] = strategy
    stats["total_chunks"] = len(docs_to_index)
    return docs_to_index, stats