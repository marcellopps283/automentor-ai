"""
AutoMentor FastAPI Server: REST API, Webhooks, and Real-Time Agent Endpoints.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from automentor.mentor_core import mentor_brain
from automentor.tools import memory_store
from automentor.api.webhooks import router as webhooks_router
from automentor.services import ingestion_service

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

# Include Webhooks Router (supports both /webhooks and /api/webhooks)
app.include_router(webhooks_router)
app.include_router(webhooks_router, prefix="/api")

# Request Models
class ChatRequest(BaseModel):
    message: str
    student_id: Optional[str] = "student_001"

class ChatResponse(BaseModel):
    reply: str
    tools_executed: List[str]
    mode: str

class IngestTextRequest(BaseModel):
    content: Optional[str] = None
    raw_text: Optional[str] = None
    source_name: Optional[str] = "Documento de Aula"

@app.get("/")
def root():
    return {
        "service": "AutoMentor AI API",
        "name": "AutoMentor AI",
        "status": "online",
        "model": "Gemini 3.5 Flash",
        "framework": "Google Agent Development Kit (ADK)",
        "endpoints": {
            "chat": "/api/chat",
            "knowledge_graph": "/api/graph",
            "ingest_text": "/api/ingest/text",
            "ingest_pdf": "/api/ingest/pdf",
            "github_webhook": "/webhooks/github",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "automentor-api"}

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

@app.post("/api/ingest/text")
def ingest_text_material(req: IngestTextRequest):
    """
    Ingests raw text (syllabus, notes) and extracts concepts into the Knowledge Graph.
    """
    text_content = req.content or req.raw_text or ""
    topics = ingestion_service.parse_syllabus(text_content, req.source_name or "Texto de Estudo")
    return {
        "status": "success",
        "source": req.source_name,
        "topics_registered": [t["topic_name"] for t in topics],
        "details": topics
    }

@app.post("/api/ingest/pdf")
async def ingest_pdf_material(
    file: UploadFile = File(...),
    source_name: Optional[str] = Form("Slide de Aula (PDF)")
):
    """
    Uploads and parses a PDF document (slides, syllabus, lecture notes)
    using pypdf and extracts knowledge nodes via Gemini 3.5.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="O arquivo enviado deve ser um PDF válido.")

    file_bytes = await file.read()
    extracted_text = ingestion_service.extract_text_from_pdf(file_bytes)
    
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Não foi possível extrair texto legível deste PDF.")

    topics = ingestion_service.parse_syllabus(extracted_text, file.filename)
    return {
        "status": "success",
        "filename": file.filename,
        "topics_registered": [t["topic_name"] for t in topics],
        "details": topics
    }

def start_server():
    import uvicorn
    uvicorn.run("automentor.api.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start_server()
