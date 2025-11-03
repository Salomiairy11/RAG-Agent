import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAI

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

import redis


load_dotenv()

pinecone_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_key)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

INDEX_NAME = "langchainvector"
vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

gemini_key = os.getenv("GOOGLE_API_KEY")

REDIS_URL = os.environ.get("REDIS_URL")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

user_input = input("Enter your name: ").strip()
SESSION_ID = f"user:{user_input}" 

def retrieve_context(query: str, top_k: int = 3) -> str:
    """Search Pinecone and return combined text context."""
    docs = vectorstore.similarity_search(query, k=top_k)
    context = "\n\n".join([d.page_content for d in docs])
    return context


def get_chat_history(session_id: str) -> str:
    """Retrieve chat history from Redis."""
    messages = redis_client.lrange(session_id, 0, -1)
    return "\n".join(messages) if messages else ""


def save_to_history(session_id: str, role: str, message: str):
    """Store a new chat message in Redis."""
    redis_client.rpush(session_id, f"{role.title()}: {message}")


def generate_response(query: str, session_id: str = SESSION_ID) -> str:
    """Custom RAG logic: retrieve + memory + LLM"""
    context = retrieve_context(query)
    chat_history = get_chat_history(session_id)

    prompt = f"""
    You are a helpful assistant that answers based on both context and conversation history.

    Context:
    {context}

    Conversation so far:
    {chat_history}

    User: {query}
    Assistant:
    """

    llm = GoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,
        google_api_key=gemini_key
    )
    response = llm.invoke(prompt)

    # save conversation back to Redis
    save_to_history(session_id, "user", query)
    save_to_history(session_id, "assistant", response)

    return response

print("Start chatting with your RAG agent. Type 'exit' to quit.\n")

while True:
    user_query = input("You: ")
    if user_query.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break
    answer = generate_response(user_query, SESSION_ID)
    print("Agent:", answer, "\n")