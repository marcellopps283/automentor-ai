"""
Suite 3: Knowledge Graph, Memory & State Transitions Deep Tests
Tests the student's mastery graph, state lifecycles, and persistence mechanisms.
"""

import pytest
from automentor.tools import update_knowledge_node, memory_store

def test_knowledge_node_lifecycle_progression():
    """
    Tests complete lifecycle of a concept:
    1. not_started (0.0) -> 2. in_progress (0.2) -> 3. gap (0.4) -> 4. in_progress (0.7) -> 5. mastered (1.0)
    """
    topic_id = "lifecycle_test_concurrency"
    topic_name = "Concorrência em Sistemas Operacionais"

    # Step 1: Initial Discovery
    n1 = update_knowledge_node(topic_id, topic_name, "in_progress", 0.2, "Conceito descoberto no slide.")
    assert "0.20" in n1

    # Step 2: Diagnostic reveals a gap
    n2 = update_knowledge_node(topic_id, topic_name, "gap", 0.35, "Aluno errou questão sobre Mutex vs Semaphore.")
    assert "GAP" in n2
    assert "0.35" in n2

    # Step 3: Practice in lab
    n3 = update_knowledge_node(topic_id, topic_name, "in_progress", 0.75, "Aluno completou lab básico com sucesso.")
    assert "IN_PROGRESS" in n3
    assert "0.75" in n3

    # Step 4: Full Mastery
    n4 = update_knowledge_node(topic_id, topic_name, "mastered", 1.0, "PR aprovado sem erros de deadlock.")
    assert "MASTERED" in n4
    assert "1.00" in n4

    # Verify state in store
    all_topics = memory_store.get_all_topics()
    saved = next(t for t in all_topics if t["topic_id"] == topic_id)
    assert saved["status"] == "mastered"
    assert saved["mastery_score"] == 1.0

def test_knowledge_graph_filtering():
    """
    Tests filtering mastered vs gap topics in the knowledge graph.
    """
    update_knowledge_node("topic_gap_1", "Deadlock Prevention", "gap", 0.3)
    update_knowledge_node("topic_gap_2", "Raft Consensus", "gap", 0.25)
    update_knowledge_node("topic_mastered_1", "HTTP/2 Multiplexing", "mastered", 1.0)

    topics = memory_store.get_all_topics()
    gap_topics = [t for t in topics if t.get("status") == "gap"]
    mastered_topics = [t for t in topics if t.get("status") == "mastered"]

    assert len(gap_topics) >= 2
    assert len(mastered_topics) >= 1

def test_knowledge_graph_notes_preservation():
    """
    Ensures Socratic feedback and educator notes are properly retained.
    """
    note_text = "Aluno demonstrou bom entendimento de latência mas precisa rever serialização binária."
    update_knowledge_node("topic_note_test", "Benchmarking REST vs gRPC", "in_progress", 0.6, note_text)

    topics = memory_store.get_all_topics()
    node = next(t for t in topics if t["topic_id"] == "topic_note_test")
    assert node["notes"] == note_text

def test_knowledge_graph_batch_updates():
    """
    Tests rapid batch registration of university syllabus concepts.
    """
    syllabus = [
        ("redis_caching", "Estratégias de Cache com Redis", "in_progress", 0.3),
        ("kafka_streaming", "Event Streaming com Apache Kafka", "not_started", 0.1),
        ("sql_indexing", "Otimização de Índices B-Tree em PostgreSQL", "mastered", 0.95),
        ("graphql_resolvers", "GraphQL Schema & N+1 Problem", "gap", 0.4)
    ]

    for tid, name, status, score in syllabus:
        res = update_knowledge_node(tid, name, status, score)
        assert tid in res.lower() or name in res

    topics = memory_store.get_all_topics()
    registered_ids = [t["topic_id"] for t in topics]
    for tid, _, _, _ in syllabus:
        assert tid in registered_ids
