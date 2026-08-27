import pytest
from automentor.mentor_core import mentor_brain
from automentor.tools import memory_store, update_knowledge_node, schedule_study_session, create_github_lab, generate_linkedin_showcase

def test_memory_store():
    res = update_knowledge_node("test_topic", "Test Topic", "gap", 0.3, "Testing notes")
    assert "Knowledge Graph atualizado" in res
    topics = memory_store.get_all_topics()
    assert any(t.get("topic_id") == "test_topic" for t in topics)

def test_calendar_tool():
    res = schedule_study_session("Test Lab", duration_minutes=30)
    assert "[Google Calendar]" in res
    assert "30 min" in res

def test_github_tool():
    res = create_github_lab("lab-test-repo", "Test Topic", "Complete the tests")
    assert "[GitHub Lab Generator]" in res
    assert "lab-test-repo" in res

def test_showcase_tool():
    res = generate_linkedin_showcase("Test Skill", "Learned something cool", "https://github.com/student/test")
    assert "[LinkedIn Showcase]" in res
    assert "Test Skill" in res

def test_mentor_brain_turn():
    mentor_brain.start_session()
    res = mentor_brain.send_message("Tenho prova de gRPC semana que vem")
    assert "reply" in res
    assert len(res["reply"]) > 10
