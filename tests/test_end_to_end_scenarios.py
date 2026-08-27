"""
Suite 6: End-to-End Integration & Golden Path Scenarios
Simulates the entire autonomous lifecycle from initial syllabus upload to 1-click LinkedIn showcase.
"""

import pytest
from fastapi.testclient import TestClient
from automentor.api.server import app

client = TestClient(app)

def test_full_autonomous_golden_path(sample_pr_diff_perfect: str):
    """
    The Full Hackathon Golden Path (3-Minute Story):
    1. Student ingests syllabus content.
    2. Student chats with Mentor regarding gRPC and Protobuf.
    3. Mentor detects initial gap -> Schedules Calendar session -> Creates GitHub Lab repo.
    4. Student solves lab and opens a Pull Request on GitHub.
    5. GitHub Webhook triggers automated PR Review via Gemini 3.5.
    6. Code passes 100% -> Knowledge Graph updated to Mastered (1.0).
    7. 1-Click LinkedIn showcase draft is ready for student approval.
    """
    # 1. Ingest Syllabus
    ingest_res = client.post(
        "/api/ingest/text",
        json={"content": "• gRPC & Protocol Buffers\n• REST APIs", "source_name": "Sistemas Distribuídos"}
    )
    assert ingest_res.status_code == 200

    # 2. Chat with Socratic Mentor
    chat_res = client.post(
        "/api/chat",
        json={"message": "Tenho prova de gRPC e Protocol Buffers semana que vem!"}
    )
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert "reply" in chat_data

    # 3. Inspect Knowledge Graph state (Gap / In Progress)
    graph_res = client.get("/api/graph")
    assert graph_res.status_code == 200
    graph_data = graph_res.json()
    assert graph_data["count"] >= 1

    # 4. Student solves challenge and submits PR via Webhook
    webhook_payload = {
        "action": "opened",
        "pull_request": {
            "number": 1,
            "title": "feat: implement grpc protobuf serializer",
            "diff_url": "https://github.com/marcello/lab-grpc/pull/1.diff"
        },
        "repository": {
            "name": "lab-grpc-protobuf-contracts",
            "full_name": "marcellopps283/lab-grpc-protobuf-contracts"
        },
        "diff_content": sample_pr_diff_perfect
    }
    webhook_res = client.post(
        "/webhooks/github",
        json=webhook_payload,
        headers={"X-GitHub-Event": "pull_request"}
    )
    assert webhook_res.status_code == 200
    webhook_data = webhook_res.json()
    
    # 5. Assert evaluation result
    assert webhook_data["status"] == "success"
    eval_result = webhook_data["evaluation"]
    assert eval_result["passed"] is True
    assert eval_result["score"] >= 0.90
    assert eval_result["showcase"] != ""

    # 6. Verify Knowledge Graph updated to Mastered
    final_graph_res = client.get("/api/graph")
    final_graph = final_graph_res.json()
    mastered_nodes = [t for t in final_graph["topics"] if t.get("status") == "mastered"]
    assert len(mastered_nodes) >= 1

def test_api_openapi_and_cloud_run_compliance():
    """
    Tests OpenAPI schema generation and healthcheck for Google Cloud Run container readiness.
    """
    openapi_res = client.get("/openapi.json")
    assert openapi_res.status_code == 200
    schema = openapi_res.json()
    assert schema["info"]["title"] == "AutoMentor AI API"
    assert "/api/chat" in schema["paths"]
    assert "/webhooks/github" in schema["paths"]
    assert "/api/graph" in schema["paths"]
    assert "/api/ingest/pdf" in schema["paths"]
