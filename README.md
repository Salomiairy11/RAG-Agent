# Conversational RAG & Document Ingestion API

Two FastAPI endpoints:

- **Document Ingestion API** – Upload documents, generate embeddings, and store metadata.
- **Conversational RAG API** – Multi-turn retrieval-augmented conversation with chat memory and interview booking support.

---

## Features

### Document Ingestion API

- **Upload .pdf or .txt files**  
  ![Upload Files](screenshots/uploadFile.PNG)

- **Extract text and apply any of the two chunking strategies:**

  - Recursive Character Chunking
  - LLM Semantic Chunking  
    ![Text Chunking](screenshots/chunking.PNG)

- **Generate embeddings and store in Pinecone vector database**

  ![Embeddings](screenshots/vectorembeddingsPinecone.PNG)

- **Save metadata in PostgreSQL**

  ![PostgreSQL](screenshots/metadataPostgres.PNG)

### Conversational RAG API

- **Custom RAG pipeline (no RetrievalQAChain)**

  ![RAG Pipeline](screenshots/chatWithAgent.PNG)

  ![AGENT-RESPONSE](screenshots/agentResponse.PNG)

- **Handles multi-turn queries with chat memory stored in Redis**

  ![Chat Memory](screenshots/redisChatHistory.PNG)

- **Supports interview booking (name, email, date, time)**

  ![Booking](screenshots/setBooking.PNG)

  ![Booking](screenshots/agentBookingConfirm.PNG)

  ![Booking](screenshots/bookingStoreInPostgres.PNG)

---

## Tech Stack

- **Backend:** FastAPI
- **Vector Database:** Pinecone
- **Chat Memory:** Redis
- **Database:** PostgreSQL
- **Python Libraries:** Pydantic, LangChain, PyPDF2, requests

---
