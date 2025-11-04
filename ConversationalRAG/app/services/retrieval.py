from ..config import get_vectorstore


def retrieve_context(query: str, top_k: int = 3) -> str:
    vectorstore = get_vectorstore()
    if not vectorstore:
        return "vectorstore not available"
    docs = vectorstore.similarity_search(query, k=top_k)
    return "\n\n".join([d.page_content for d in docs])
