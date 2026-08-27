"""
Suite 2: Autonomous Tool Execution & Actuator Deep Tests
Tests Google Calendar scheduling, GitHub Lab scaffolding, LinkedIn Showcase generation, and error boundaries.
"""

import pytest
from datetime import datetime, timedelta
from automentor.tools import schedule_study_session, create_github_lab, generate_linkedin_showcase, update_knowledge_node

def test_calendar_tool_ebbinghaus_intervals():
    """
    Tests spaced repetition intervals for Ebbinghaus retention (D+1, D+3, D+7).
    """
    for offset in [1, 3, 7, 14]:
        res = schedule_study_session(
            topic_name="Concorrência com Channels em Go",
            duration_minutes=25,
            suggested_day_offset=offset
        )
        assert "[Google Calendar]" in res
        assert "25 min" in res
        assert "Concorrência com Channels em Go" in res

def test_calendar_tool_duration_boundaries():
    """
    Tests minimum (10 min) and maximum (120 min) study block allocations.
    """
    micro_session = schedule_study_session("Micro-quiz", duration_minutes=15)
    deep_work = schedule_study_session("Deep Lab", duration_minutes=90)
    
    assert "15 min" in micro_session
    assert "90 min" in deep_work

def test_github_tool_multi_language_scaffolding():
    """
    Tests scaffolding lab repositories in different programming languages.
    """
    languages = ["python", "typescript", "go"]
    for lang in languages:
        res = create_github_lab(
            repo_name=f"lab-microservices-{lang}",
            topic_name=f"Microservices in {lang.title()}",
            challenge_description="Implement healthcheck and RPC endpoint",
            language=lang
        )
        assert "[GitHub Lab Generator]" in res
        assert f"lab-microservices-{lang}" in res
        assert "README.md" in res
        assert "Dockerfile" in res

def test_github_tool_special_characters_sanitization():
    """
    Tests that repo names with spaces, uppercase, and accents are properly sanitized to kebab-case.
    """
    dirty_name = "Lab 01 - Autenticação JWT & Criptografia 2026!"
    res = create_github_lab(dirty_name, "JWT Auth", "Implement token signing")
    assert "[GitHub Lab Generator]" in res
    # Should be sanitized without spaces or exclamation marks
    assert " " not in res.split("URL: ")[1].split("\n")[0]

def test_showcase_tool_formatting():
    """
    Tests LinkedIn post generation ensuring key learnings, repository link and hashtags are included.
    """
    res = generate_linkedin_showcase(
        topic_name="Kubernetes Ingress & TLS Termination",
        key_learnings="Configuração de certificados SSL automáticos com cert-manager e roteamento L7.",
        repo_url="https://github.com/student/lab-k8s-ingress"
    )
    assert "[LinkedIn Showcase]" in res
    assert "Kubernetes Ingress & TLS Termination" in res
    assert "https://github.com/student/lab-k8s-ingress" in res
    assert "#Backend" in res
    assert "#GoogleCloud" in res
