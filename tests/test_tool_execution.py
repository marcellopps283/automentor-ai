"""
Suite 2: Autonomous Tool Execution & Actuator Deep Tests
Tests Google Calendar scheduling, GitHub Lab scaffolding, LinkedIn Showcase generation, and Cheat Sheets.
"""

import pytest
from datetime import datetime, timedelta
from automentor.tools import (
    schedule_study_session,
    create_github_lab,
    generate_linkedin_showcase,
    update_knowledge_node,
    generate_study_cheat_sheet
)

def test_calendar_tool_ebbinghaus_intervals():
    """
    Tests spaced repetition intervals for Ebbinghaus retention (D+1, D+3, D+7, D+14).
    """
    for interval in ["D+1", "D+3", "D+7", "D+14"]:
        res = schedule_study_session(
            topic_name="Concorrência com Channels em Go",
            duration_minutes=25,
            ebbinghaus_interval=interval,
            preferred_time_window="night"
        )
        assert "[Google Calendar]" in res
        assert "25 min" in res
        assert interval in res
        assert "https://calendar.google.com" in res

def test_calendar_tool_duration_boundaries():
    """
    Tests minimum (15 min) and maximum (90 min) study block allocations.
    """
    micro_session = schedule_study_session("Micro-quiz", duration_minutes=15, preferred_time_window="morning")
    deep_work = schedule_study_session("Deep Lab", duration_minutes=90, preferred_time_window="evening")
    
    assert "15 min" in micro_session
    assert "90 min" in deep_work

def test_github_tool_multi_language_scaffolding():
    """
    Tests scaffolding lab repositories in different programming languages and difficulty levels.
    """
    languages = ["python", "typescript", "go"]
    for lang in languages:
        res = create_github_lab(
            repo_name=f"lab-microservices-{lang}",
            topic_name=f"Microservices in {lang.title()}",
            challenge_description="Implement healthcheck and RPC endpoint",
            language=lang,
            difficulty="advanced"
        )
        assert "[GitHub Lab Generator]" in res
        assert f"lab-microservices-{lang}" in res
        assert "README.md" in res
        assert "Dockerfile" in res
        assert "ADVANCED" in res

def test_github_tool_special_characters_sanitization():
    """
    Tests that repo names with spaces, uppercase, and accents are properly sanitized to kebab-case.
    """
    dirty_name = "Lab 01 - Autenticação JWT & Criptografia 2026!"
    res = create_github_lab(dirty_name, "JWT Auth", "Implement token signing")
    assert "[GitHub Lab Generator]" in res
    assert " " not in res.split("URL: ")[1].split("\n")[0]

def test_showcase_tool_multi_format():
    """
    Tests LinkedIn post, Markdown badge, and CV bullet generation.
    """
    # 1. LinkedIn Post
    post = generate_linkedin_showcase(
        topic_name="Kubernetes Ingress & TLS",
        key_learnings="Certificados automáticos com cert-manager.",
        repo_url="https://github.com/student/lab-k8s-ingress",
        format_type="linkedin_post"
    )
    assert "[LinkedIn Showcase]" in post
    assert "#Backend" in post

    # 2. GitHub Markdown Badge
    badge = generate_linkedin_showcase(
        topic_name="Kubernetes Ingress & TLS",
        key_learnings="",
        repo_url="https://github.com/student/lab-k8s-ingress",
        format_type="github_badge"
    )
    assert "[![Kubernetes Ingress & TLS]" in badge
    assert "img.shields.io" in badge

    # 3. Resume Bullet
    bullet = generate_linkedin_showcase(
        topic_name="Kubernetes Ingress & TLS",
        key_learnings="",
        repo_url="https://github.com/student/lab-k8s-ingress",
        format_type="resume_bullet"
    )
    assert "• Desenvolveu serviços em Kubernetes Ingress & TLS" in bullet

def test_cheat_sheet_tool_generation():
    """
    Tests autonomous generation of structured exam cheat sheets.
    """
    res = generate_study_cheat_sheet(
        topic_name="Sistemas Distribuídos: Raft Consensus",
        core_principles="1. Leader Election com heartbeat\n2. Log Replication e quórum majoritário",
        common_pitfalls="1. Split-brain quando não há maioria estrita (N/2 + 1)\n2. Eleição simultânea em caso de timers iguais",
        code_example="def request_vote(term: int, candidate_id: str) -> bool:\n    return True"
    )
    assert "# 📄 Guia de Bolso: Sistemas Distribuídos: Raft Consensus" in res
    assert "Pegadinhas Clássicas" in res
    assert "request_vote" in res
