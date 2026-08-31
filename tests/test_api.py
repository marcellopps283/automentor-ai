"""
FastAPI Server Endpoints and Webhooks Tests
"""

import pytest
from fastapi.testclient import TestClient
from automentor.api.server import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "AutoMentor" in data.get("name", "") or "AutoMentor" in data.get("service", "")
    assert data.get("status") in ["online", "running"]

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_chat_endpoint():
    payload = {
        "message": "Estou com dúvida em gRPC e Protobufs para a prova.",
        "student_id": "test_student"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["reply"]) > 10

def test_knowledge_graph_endpoint():
    response = client.get("/api/graph")
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data
    assert isinstance(data["topics"], list)

def test_ingest_text_endpoint():
    payload = {
        "raw_text": "Sistemas Distribuídos: gRPC, RPC, Sockets, Raft Consensus.",
        "source_name": "Ementa 2026"
    }
    response = client.post("/api/ingest/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["topics_registered"]) >= 1

def test_ingest_pdf_endpoint():
    files = {"file": ("aula_sistemas.pdf", b"Sistemas Distribuidos e Microservicos gRPC", "application/pdf")}
    response = client.post("/api/ingest/pdf", files=files, data={"source_name": "Aula 01"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_github_webhook_endpoint():
    webhook_payload = {
        "action": "opened",
        "pull_request": {
            "title": "feat: implement grpc serialization",
            "body": "Resolvendo o desafio prático de gRPC",
            "diff_url": "https://github.com/student/lab-grpc/pull/1.diff",
            "comments_url": "https://api.github.com/repos/student/lab-grpc/issues/1/comments",
            "user": {"login": "student_marcelo"}
        },
        "repository": {
            "name": "lab-grpc-contracts",
            "full_name": "student/lab-grpc-contracts"
        }
    }
    response = client.post(
        "/api/webhooks/github",
        json=webhook_payload,
        headers={"X-GitHub-Event": "pull_request"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["success", "reviewed"]
    assert "evaluation" in data
