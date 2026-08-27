"""
Suite 4: Pull Request Evaluator & Code Review Deep Tests
Tests automated code review, Socratic critique, diff parsing, and GitHub commenting.
"""

import pytest
from automentor.services import pr_evaluator

def test_pr_evaluator_perfect_submission(sample_pr_diff_perfect: str):
    """
    Scenario: Student submits clean code that satisfies all challenge unit tests.
    Expected: Evaluator marks passed=True, score >= 0.90, gives praise and generates LinkedIn showcase draft.
    """
    result = pr_evaluator.evaluate_code_diff(
        topic_id="grpc_serialization",
        topic_name="Serialização gRPC & Protobuf",
        code_diff=sample_pr_diff_perfect,
        pr_title="feat: implement Protobuf byte serializer"
    )

    assert result["passed"] is True
    assert result["score"] >= 0.90
    assert "Excelente trabalho" in result["feedback"] or "parabéns" in result["feedback"].lower()
    assert result["showcase"] != ""

def test_pr_evaluator_buggy_submission(sample_pr_diff_buggy: str):
    """
    Scenario: Student submits code with unfinished logic or missing validation.
    Expected: Evaluator marks passed=False, score <= 0.50, provides Socratic hint rather than giving raw answer.
    """
    result = pr_evaluator.evaluate_code_diff(
        topic_id="grpc_serialization",
        topic_name="Serialização gRPC & Protobuf",
        code_diff=sample_pr_diff_buggy,
        pr_title="wip: partial serializer"
    )

    assert result["passed"] is False
    assert result["score"] <= 0.50
    assert "Pergunta Socrática" in result["feedback"] or "ajuda" in result["feedback"].lower()
    assert result["showcase"] == ""

def test_pr_evaluator_empty_diff_handling():
    """
    Scenario: Student opens a PR with no code changes (empty diff).
    Expected: Handled gracefully without raising unhandled exceptions.
    """
    result = pr_evaluator.evaluate_code_diff(
        topic_id="empty_lab",
        topic_name="Empty Lab",
        code_diff="",
        pr_title="empty pr"
    )
    assert result is not None
    assert result["passed"] is False

def test_pr_evaluator_github_comment_generation():
    """
    Tests posting or formatting of the review comment to a GitHub PR.
    """
    status = pr_evaluator.post_pr_comment(
        repo_full_name="student/lab-grpc-protobuf",
        pr_number=42,
        comment_body="🎉 Testes passaram 100%! Habilidade consolidada."
    )
    assert "42" in status
    assert "student/lab-grpc-protobuf" in status
