from datetime import datetime
from typing import List, Dict, Any
from langchain_core.documents import Document

def build_metadata(docs_to_index: List[Document], filename: str) -> List[Dict[str, Any]]:
    """
    Build structured metadata for a list of LangChain Document chunks.

    Args:
        docs_to_index (List[Document]): 
            List of Document objects representing the text chunks to be indexed.
        filename (str): 
            The original source filename for the document.

    Returns:
        List[Dict[str, Any]]: 
            A list of metadata dictionaries containing indexing details.
    """
    metadata_list: List[Dict[str, Any]] = []
    for doc in docs_to_index:
        metadata_list.append(
            {
                "chunk_index": doc.metadata.get("chunk_index"),
                "chunk_strategy": doc.metadata.get("strategy"),
                "chunk_filename": filename,
                "created_at": datetime.now(),
            }
        )
    return metadata_list