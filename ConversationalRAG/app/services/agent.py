import logging
import re
from datetime import datetime
from typing import Any, Dict

from .retrieval import retrieve_context
from .chat_history import get_chat_history, save_to_history
from .generation import generate_llm_response
from .booking import handle_booking
from ..config import get_redis_client

logger = logging.getLogger(__name__)
REQUIRED_BOOKING_FIELDS = ["name", "email", "date", "time"]


# VALIDATION LOGIC FOR EACH FIELD
def is_valid_email(email: str) -> bool:
    """Simple email validation."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))        

def is_valid_date(date_str: str) -> bool:
    """Check if date is in YYYY-MM-DD format"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_time(time_str: str) -> bool:
    """Check if time is in HH:MM 24-hour format."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False



# BOOKING AND CHAT ORCHESTRATION
def chat_with_agent(user_query: str, session_id: str)-> str:
    """
    Main orchestrator handling both chat and booking interactions.
    - Detects booking intent
    - Collects booking details progressively via Redis
    - Falls back to RAG chat if no booking is in progress
    """
    
    user_query = user_query.lower()
    redis_client = get_redis_client()

    booking_state_key = f"booking_state:{session_id}"
    booking_data = redis_client.hgetall(booking_state_key)

    if any(keyword in user_query for keyword in ["book interview", "schedule interview", "set interview"]):
        redis_client.delete(booking_state_key)
        redis_client.hset(booking_state_key, mapping={"progress": "name"})
        response = "Sure! Let's book your interview. What's your full name?"
        save_to_history(session_id, "assistant", response)
        return response

    if booking_data:
        progress = booking_data.get("progress")

        if progress == "name":
            redis_client.hset(booking_state_key, mapping={"name": user_query, "progress": "email"})
            response = "Got it. Could you provide your email address?"
            save_to_history(session_id, "assistant", response)
            return response

        elif progress == "email":
            if not is_valid_email(user_query):
                response = "Hmm, that doesn’t look like a valid email. Please provide a valid email address (e.g., john@example.com)."
                save_to_history(session_id, "assistant", response)
                return response

            redis_client.hset(booking_state_key, mapping={"email": user_query, "progress": "date"})
            response = "Thanks! What date would you like for the interview? (Format: YYYY-MM-DD)"
            save_to_history(session_id, "assistant", response)
            return response

        elif progress == "date":
            if not is_valid_date(user_query):
                response = "That date doesn’t look right. Please provide a valid date in YYYY-MM-DD format."
                save_to_history(session_id, "assistant", response)
                return response

            redis_client.hset(booking_state_key, mapping={"date": user_query, "progress": "time"})
            response = "Perfect. What time works best for you? (Format: HH:MM in 24-hour time)"
            save_to_history(session_id, "assistant", response)
            return response

        elif progress == "time":
            if not is_valid_time(user_query):
                response = "Please provide a valid time in 24-hour format (e.g., 14:30)."
                save_to_history(session_id, "assistant", response)
                return response

            # All details collected — finalize booking
            redis_client.hset(booking_state_key, mapping={"time": user_query})
            data = redis_client.hgetall(booking_state_key)

            response = handle_booking(
                name=data["name"],
                email=data["email"],
                date=data["date"],
                time=data["time"]
            )

            redis_client.delete(booking_state_key)
            save_to_history(session_id, "assistant", response)
            return response

    # Normal RAG Chat (no booking intent)
    context = retrieve_context(user_query)
    chat_history = get_chat_history(session_id)

    prompt = f"""
    You are a helpful assistant. Answer questions using the provided context and conversation history. Keep responses clear, accurate, and relevant.

    Context:
    {context}

    Conversation so far:
    {chat_history}

    User: {user_query}
    Assistant:
    """

    response = generate_llm_response(prompt)
    save_to_history(session_id, "user", user_query)
    save_to_history(session_id, "assistant", response)
    return response
