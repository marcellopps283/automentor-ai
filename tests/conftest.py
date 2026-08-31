"""
Pytest Fixtures and Mock Data for AutoMentor AI Test Battery
"""

import pytest
import io
from typing import Dict, Any
from automentor.mentor_core import MentorBrain
from automentor.tools import MemoryStore

@pytest.fixture
def mock_student_profile() -> Dict[str, Any]:
    return {
        "student_id": "student_marcelo_001",
        "name": "Marcelo Paiva",
        "career_goal": "Senior Backend & Cloud Engineer",
        "current_semester": 6,
        "college_course": "Ciência da Computação",
        "active_courses": [
            "Sistemas Distribuídos",
            "Banco de Dados Avançado",
            "Compiladores"
        ]
    }

@pytest.fixture
def clean_memory_store(tmp_path) -> MemoryStore:
    """Returns an isolated MemoryStore using a temporary JSON file."""
    store = MemoryStore()
    store.use_firestore = False
    return store

@pytest.fixture
def mentor_instance() -> MentorBrain:
    brain = MentorBrain(model_name="gemini-3.5-flash")
    brain.start_session()
    return brain

@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """Generates valid 1-page PDF bytes containing a mock Distributed Systems syllabus."""
    try:
        from pypdf import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=300)
        buf = io.BytesIO()
        writer.write(buf)
    except ImportError:
        pass
    # Return valid PDF header + text
    return b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/Contents 4 0 R>>endobj\n4 0 obj<</Length 55>>stream\nBT /F1 12 Tf 50 250 Td (Sistemas Distribuidos: gRPC, RPC, Sockets, Raft) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000056 00000 n \n0000000111 00000 n \n0000000173 00000 n \ntrailer<</Size 5/Root 1 0 R>>\nstartxref\n279\n%%EOF"

@pytest.fixture
def sample_pr_diff_perfect() -> str:
    return """
diff --git a/challenge.py b/challenge.py
index 1234567..89abcdef 100644
--- a/challenge.py
+++ b/challenge.py
@@ -5,6 +5,10 @@ def solve_grpc_contracts(input_data: dict) -> dict:
-    raise NotImplementedError("Implemente esta função para resolver o desafio!")
+    if not input_data or not input_data.get("id"):
+        raise ValueError("Payload inválido: id obrigatório")
+    
+    return {
+        "status": "success",
+        "serialized_bytes": b"\\x08\\x96\\x01\\x12\\x07marcelo",
+        "tag_count": len(input_data)
+    }
"""

@pytest.fixture
def sample_pr_diff_buggy() -> str:
    return """
diff --git a/challenge.py b/challenge.py
index 1234567..89abcdef 100644
--- a/challenge.py
+++ b/challenge.py
@@ -5,6 +5,8 @@ def solve_grpc_contracts(input_data: dict) -> dict:
-    raise NotImplementedError("Implemente esta função para resolver o desafio!")
+    # Aluno esqueceu de validar entrada e retorna None
+    return None
"""
