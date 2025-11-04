from ..config import get_redis_client

redis_client = get_redis_client()

def get_chat_history(session_id: str) -> str:
    if not redis_client:
        return "redis client not available"
    messages = redis_client.lrange(session_id, 0, -1)
    return "\n".join(messages) if messages else ""

def save_to_history(session_id: str, role: str, message: str):
    if not redis_client:
        return "redis client not available"
    redis_client.rpush(session_id, f"{role.title()}: {message}")
