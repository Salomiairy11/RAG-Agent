from fastapi import APIRouter
from .services.agent import chat_with_agent

router = APIRouter()

@router.post("/agent")
def converse_with_agent(user_query: str, session_id: str):
    response = chat_with_agent(user_query, session_id)
    return {"response": response}
