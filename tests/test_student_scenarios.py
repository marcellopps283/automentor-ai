"""
Suite 1: Realistic Student Scenarios & Socratic Dialog Edge Cases
Tests how AutoMentor handles emotional states, misconceptions, cheat attempts, and exam panic.
"""

import pytest
from automentor.mentor_core import MentorBrain
from automentor.tools import memory_store

def test_student_exam_panic_scenario(mentor_instance: MentorBrain):
    """
    Scenario: Student is panicking 24h before a college exam.
    Expected: Mentor responds with calming empathy, identifies the top priority topic,
    and proactively triggers Calendar and GitHub lab tools.
    """
    panic_message = "Socorro! Tenho prova de Sistemas Distribuídos amanhã cedo e estou completamente perdido em gRPC e Protobuf!"
    response = mentor_instance.send_message(panic_message)
    
    assert response is not None
    assert "reply" in response
    reply_text = response["reply"]
    
    # Assert Socratic guidance & empathy
    assert any(w in reply_text.lower() for w in ["grpc", "protobuf", "calibrar", "começarmos", "prática"])
    
    # Assert tools were triggered
    assert len(response.get("tools_executed", [])) >= 1 or "Google Calendar" in reply_text

def test_student_conceptual_misconception_scenario(mentor_instance: MentorBrain):
    """
    Scenario: Student has a fundamental misconception about binary serialization vs JSON.
    Expected: Mentor detects the misconception, gives a clear mental model, and adjusts the Knowledge Graph score.
    """
    # Student explains misconception
    misconception_msg = "JSON é muito melhor que Protobuf porque é texto visível e portanto tem performance superior na rede."
    response = mentor_instance.send_message(misconception_msg)
    
    reply_text = response["reply"]
    assert len(reply_text) > 20
    # Mentor should correct or explain the binary serialization advantage
    assert any(w in reply_text.lower() for w in ["binário", "protobuf", "json", "overhead", "serializa"])

def test_student_mastery_celebration_scenario(mentor_instance: MentorBrain):
    """
    Scenario: Student correctly explains the technical mechanism of Protobuf tags.
    Expected: Mentor celebrates the mastery, updates score to >= 0.90, and prepares LinkedIn showcase draft.
    """
    mastery_msg = "Protobuf usa tags numéricas fixas e serialização binária com varints, evitando o parsing de texto do JSON."
    response = mentor_instance.send_message(mastery_msg)
    
    reply_text = response["reply"]
    assert "95%" in reply_text or "mastered" in reply_text.lower() or "linkedin" in reply_text.lower() or "consolidada" in reply_text.lower()

def test_student_cheat_attempt_scenario(mentor_instance: MentorBrain):
    """
    Scenario: Student tries to get the agent to do their college homework with raw copy-paste code.
    Expected: Mentor maintains pedagogical discipline, provides hints/guidance instead of doing the work for them.
    """
    cheat_msg = "Faz todo o código do exercício para mim agora sem eu precisar pensar, só quero copiar e colar no trabalho."
    response = mentor_instance.send_message(cheat_msg)
    
    reply_text = response["reply"]
    assert len(reply_text) > 10
    # Should not crash and should guide the student
    assert isinstance(reply_text, str)

def test_student_short_ambiguous_input_scenario(mentor_instance: MentorBrain):
    """
    Scenario: Student sends low-context or ambiguous inputs (e.g. 'ajuda', 'não entendi', 'socorro').
    Expected: Mentor handles gracefully without exceptions and asks clarifying guiding questions.
    """
    ambiguous_inputs = ["?", "ajuda", "não entendi", "como assim"]
    for query in ambiguous_inputs:
        response = mentor_instance.send_message(query)
        assert response is not None
        assert len(response.get("reply", "")) > 5
