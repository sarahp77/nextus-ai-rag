import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from rag_service import search_knowledge

load_dotenv()

app = FastAPI(
    title="NextusAI Enterprise Assistant API",
    description="Production-grade RAG microservice with ChromaDB and OpenAI",
    version="1.0.0"
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    sources_used: bool

@app.post("/chat", response_model=ChatResponse)
def chat_with_agent(req: ChatRequest):
    try:
        
        context = search_knowledge(req.message, n_results=2)
        has_context = bool(context and "No relevant documents found" not in context)

        
        system_prompt = (
            "You are the NextusAI Enterprise Support Specialist. "
            "Answer user questions accurately and professionally based ONLY on the provided context below. "
            "If the answer cannot be found in the context, politely state that you do not have that information.\n\n"
            f"--- Context ---\n{context if has_context else 'No context available.'}"
        )

       
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ],
            temperature=0.2
        )

        return ChatResponse(
            reply=response.choices[0].message.content,
            sources_used=has_context
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
