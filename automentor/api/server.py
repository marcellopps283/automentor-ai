"""
AutoMentor FastAPI Server: REST API, Webhooks, and Real-Time Agent Endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from automentor.mentor_core import mentor_brain
from automentor.tools import memory_store
from automentor.api.webhooks import router as webhooks_router

app = FastAPI(
    title="AutoMentor AI API",
    description="Backend API and Autonomous Webhook Engine for AutoMentor AI (All Things Agentic Hackathon)",
    version="0.1.0"
)

# Enable CORS for local & cloud frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Webhooks Router
app.include_router(webhooks_router)

# Request Models
class ChatRequest(BaseModel):
    message: str
    student_id: Optional[str] = "student_001"

class ChatResponse(BaseModel):
    reply: str
    tools_executed: List[str]
    mode: str

class IngestRequest(BaseModel):
    content: str
    source_name: Optional[str] = "Documento de Aula"

@app.get("/")
def root():
    return {
        "service": "AutoMentor AI API",
        "status": "online",
        "model": "Gemini 3.5 Flash",
        "framework": "Google Agent Development Kit (ADK)",
        "endpoints": {
            "chat": "/api/chat",
            "knowledge_graph": "/api/graph",
            "github_webhook": "/webhooks/github",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_mentor(req: ChatRequest):
    """Sends a message to the Socratic Mentor and returns response and actions taken."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    res = mentor_brain.send_message(req.message)
    return ChatResponse(
        reply=res.get("reply", ""),
        tools_executed=res.get("tools_executed", []),
        mode=res.get("mode", "simulation")
    )

@app.get("/api/graph")
def get_knowledge_graph():
    """Returns the current Knowledge Graph with all topics and mastery scores."""
    topics = memory_store.get_all_topics()
    return {
        "count": len(topics),
        "topics": topics
    }

@app.post("/api/ingest")
def ingest_material(req: IngestRequest):
    """
    Ingests study materials (syllabus, notes, lecture text)
    and populates initial topics into the student's Knowledge Graph.
    """
    from automentor.tools import update_knowledge_node
    # Parse basic topics from content
    lines = [line.strip() for line in req.content.splitlines() if line.strip()]
    registered = []
    
    for idx, line in enumerate(lines[:5]):
        topic_name = line.strip("•-*#0123456789. ")
        if len(topic_name) > 3:
            topic_id = topic_name.lower().replace(" ", "_")[:30]
            update_knowledge_node(
                topic_id=topic_id,
                topic_name=topic_name,
                status="in_progress",
                score=0.2,
                notes=f"Ingerido a partir de: {req.source_name}"
            )
            registered.append(topic_name)

    return {
        "status": "success",
        "source": req.source_name,
        "topics_registered": registered
    }

def start_server():
    import uvicorn
    uvicorn.run("automentor.api.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start_server()
