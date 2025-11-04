from ..config import get_vectorstore


def retrieve_context(query: str, top_k: int = 3) -> str:
    """
    Retrieve the most relevant context documents from the vector store.

    Args:
        query (str): The search query text.
        top_k (int, optional): Number of top similar documents to return. Defaults to 3.

    Returns:
        str: Concatenated content of retrieved documents, or an error message.
    """
    vectorstore = get_vectorstore()
    if vectorstore is None:
        return "Vector store not available"

    try:
        docs = vectorstore.similarity_search(query, k=top_k)
        if not docs:
            return "No relevant context found."
        return "\n\n".join([d.page_content for d in docs])
    except Exception as e:
        return f"Error retrieving context: {e}"
    
