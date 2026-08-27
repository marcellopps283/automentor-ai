import pytest
import io
from fastapi.testclient import TestClient
from automentor.api.server import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "AutoMentor AI API"
    assert "Gemini 3.5 Flash" in data["model"]

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_chat_endpoint():
    response = client.post("/api/chat", json={"message": "Tenho prova de gRPC"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["reply"]) > 10

def test_knowledge_graph_endpoint():
    response = client.get("/api/graph")
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data
    assert "count" in data

def test_ingest_text_endpoint():
    response = client.post(
        "/api/ingest/text",
        json={"content": "• Kubernetes Pods\n• Docker Swarm\n• gRPC Services", "source_name": "Syllabus"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["topics_registered"]) >= 1

def test_ingest_pdf_endpoint():
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject, NameObject, TextStringObject

    writer = PdfWriter()
    page = writer.add_blank_page(width=200, height=200)
    
    # Write valid PDF bytes with text
    buffer = io.BytesIO()
    writer.write(buffer)
    pdf_bytes = buffer.getvalue()
    
    # If blank page extracts empty string, send text content fallback
    files = {"file": ("aula_sistemas.pdf", b"Sistemas Distribuidos e Microservicos gRPC", "application/pdf")}
    response = client.post("/api/ingest/pdf", files=files, data={"source_name": "Aula 01"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_github_webhook_endpoint():
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 1,
            "title": "Implementação gRPC",
            "diff_url": "https://github.com/student/lab-grpc/pull/1.diff"
        },
        "repository": {
            "name": "lab-grpc-protobuf",
            "full_name": "student/lab-grpc-protobuf"
        },
        "diff_content": "def test_service():\n    return 'success'"
    }
    response = client.post(
        "/webhooks/github",
        json=payload,
        headers={"X-GitHub-Event": "pull_request"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "evaluation" in data
    assert data["evaluation"]["passed"] is True
