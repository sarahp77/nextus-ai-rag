# NexusAI — Enterprise RAG Knowledge Microservice

A lightweight and robust Retrieval-Augmented Generation (RAG) backend service built with **FastAPI**, **ChromaDB**, and **OpenAI**. 

This microservice ingests enterprise documents, indexes them into a local vector database, and uses semantic search combined with strict prompt grounding to answer user queries accurately without hallucination.

## Tech Stack

- **Framework:** FastAPI, Uvicorn
- **LLM & Embeddings:** OpenAI (`gpt-4o-mini`, `text-embedding-3-small`)
- **Vector Database:** ChromaDB (Persistent local storage)
- **Text Processing:** LangChain Text Splitters
- **Validation:** Pydantic v2

---

## Project Structure
```text
nexus-ai-rag/
│
├── main.py              # FastAPI application and /chat endpoint
├── rag_service.py       # ChromaDB indexing and semantic search logic
├── knowledge_base.txt   # Enterprise documentation source
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API keys)
└── README.md            # Project documentation
```
---

## Getting Started Locally

### 1. Clone the repository and set up a virtual environment
```bash
git clone https://github.com/sarahp77/nextus-ai-rag.git
cd nexus-ai-rag
```
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Configure environment variables
Create a `.env` file in the root directory and add your API key:
env
OPENAI_API_KEY=your_actual_api_key_here

### 4. Index the Knowledge Base
Run the RAG service script once to chunk and store the documentation in ChromaDB:
```bash
python rag_service.py
```
### 5. Run the FastAPI Server
```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`. You can access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

---

## API Usage

### Endpoint: `POST /chat`

**Request Body:**
json
{
  "message": "How much is the Growth Tier and what does it include?"
}

**Response:**
json
{
  "reply": "The Growth Tier costs €49 per month and includes up to 50,000 API calls, dedicated vector database indexes, and email support.",
  "sources_used": true
}

---

## License
This project is open-source and available under the [MIT License](LICENSE).
