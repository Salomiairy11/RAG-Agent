from fastapi import FastAPI
from ConversationalRAG.app.main import router as agent_router
from DocumentIngestionAPI.app.main import router as upload_router

app = FastAPI(title="Conversational RAG API")

#Document Ingestion API
app.include_router(upload_router)

#Conversational RAG API
app.include_router(agent_router)


