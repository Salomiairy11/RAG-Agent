from ..config import get_redis_client


redis_client = get_redis_client()

def get_chat_history(session_id: str) -> str:
    """Retrieve the full chat history for a given session from Redis.

    Args:
        session_id (str): Unique session identifier.

    Returns:
        str: The chat history joined as newline-separated messages.
    """
    if not redis_client:
        return "redis client not available"
    messages = redis_client.lrange(session_id, 0, -1)
    return "\n".join(messages) if messages else ""

def save_to_history(session_id: str, role: str, message: str) -> None:
    """
    Append a new chat message to the Redis chat history.

    Args:
        session_id (str): Unique session identifier.
        role (str): Role of the speaker ('user' or 'assistant').
        message (str): Message text.
    """
    if redis_client is None:
        return
    redis_client.rpush(session_id, f"{role.title()}: {message}")
