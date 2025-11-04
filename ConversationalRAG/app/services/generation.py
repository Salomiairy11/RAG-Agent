from ..config import get_google_api_key
from langchain_google_genai import GoogleGenerativeAI

def generate_llm_response(prompt: str) -> str:
    llm = GoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,
        google_api_key=get_google_api_key()
    )
    return llm.invoke(prompt)
