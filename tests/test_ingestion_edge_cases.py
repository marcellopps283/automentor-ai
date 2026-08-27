"""
Suite 5: Document Ingestion, PDF Extraction & Syllabus Parsing Tests
Tests extraction of college slides, syllabus text, and edge cases with corrupt/multilingual files.
"""

import pytest
from automentor.services import ingestion_service

def test_pdf_text_extraction(sample_pdf_bytes: bytes):
    """
    Tests extracting text from valid PDF bytes using pypdf.
    """
    extracted_text = ingestion_service.extract_text_from_pdf(sample_pdf_bytes)
    assert extracted_text is not None
    assert isinstance(extracted_text, str)

def test_corrupt_pdf_fallback():
    """
    Scenario: Uploaded PDF is corrupt or invalid binary data.
    Expected: Ingestion service handles without crashing, falling back to raw decode.
    """
    corrupt_bytes = b"NOT_A_VALID_PDF_STREAM_CORRUPT_BYTES\x00\x01\x02"
    result = ingestion_service.extract_text_from_pdf(corrupt_bytes)
    assert result is not None
    assert isinstance(result, str)

def test_syllabus_structured_concept_extraction():
    """
    Tests extracting structured topics from a university syllabus.
    """
    syllabus_text = """
    DISCIPLINA: SISTEMAS DISTRIBUÍDOS E CLOUD COMPUTING
    EMENTA E CRONOGRAMA:
    1. Arquitetura de Microsserviços e RPC
    2. Comunicação Interprocessos com gRPC e Protocol Buffers
    3. Algoritmos de Consenso Distribuído (Raft e Paxos)
    4. Service Mesh e Observabilidade com OpenTelemetry
    5. Estratégias de Deploy Canário e Blue-Green no Kubernetes
    """
    topics = ingestion_service.parse_syllabus(syllabus_text, "Ementa Sistemas Distribuídos")
    
    assert len(topics) >= 3
    topic_names = [t["topic_name"].lower() for t in topics]
    assert any("rpc" in name or "microsserviços" in name or "distribuído" in name for name in topic_names)

def test_empty_syllabus_extraction():
    """
    Scenario: Uploaded document is empty or whitespace only.
    Expected: Handled cleanly, returning empty list without errors.
    """
    topics = ingestion_service.parse_syllabus("", "Empty Document")
    assert isinstance(topics, list)
    assert len(topics) == 0

def test_multilingual_accents_preservation():
    """
    Tests that Portuguese accents (á, é, í, ó, ú, ã, õ, ç) are properly preserved in concept titles.
    """
    accented_text = """
    • Concorrência e Programação Assíncrona
    • Transações Distribuídas e Isolamento ACID
    • Autenticação Criptográfica com Chaves Públicas
    """
    topics = ingestion_service.parse_syllabus(accented_text, "Aula 02")
    assert len(topics) >= 1
    assert any("ç" in t["topic_name"] or "ã" in t["topic_name"] or "í" in t["topic_name"] for t in topics)
