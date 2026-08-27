"""
GitHub Webhooks Handler: Receives and processes events from student lab repositories.
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
from automentor.services import pr_evaluator

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/github")
async def handle_github_webhook(request: Request) -> Dict[str, Any]:
    """
    Receives events from GitHub (e.g. pull_request.opened, pull_request.synchronize).
    Extracts the PR diff, triggers Socratic evaluation, and leaves review comments.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event_type = request.headers.get("X-GitHub-Event", "pull_request")
    action = payload.get("action", "")

    # Check if this is a Pull Request event
    if "pull_request" in payload:
        pr_data = payload["pull_request"]
        repo_data = payload.get("repository", {})
        
        pr_number = pr_data.get("number", 1)
        pr_title = pr_data.get("title", "Desafio")
        repo_full_name = repo_data.get("full_name", "student/lab-repo")
        diff_url = pr_data.get("diff_url", "")
        
        # Extract topic from title or repo name
        topic_name = repo_data.get("name", "Laboratório Prático").replace("lab-", "").replace("-", " ").title()
        topic_id = repo_data.get("name", "lab_generic").replace("lab-", "").replace("-", "_")

        # Mock or real diff text
        code_diff = payload.get("diff_content", "def solve_challenge():\n    return {'status': 'success', 'data': 'ok'}")

        # Run Evaluation
        result = pr_evaluator.evaluate_code_diff(
            topic_id=topic_id,
            topic_name=topic_name,
            code_diff=code_diff,
            pr_title=pr_title
        )

        # Post review comment to GitHub PR
        comment_status = pr_evaluator.post_pr_comment(
            repo_full_name=repo_full_name,
            pr_number=pr_number,
            comment_body=result["feedback"]
        )

        return {
            "status": "success",
            "action": action,
            "pr_number": pr_number,
            "evaluation": result,
            "github_comment": comment_status
        }

    return {"status": "ignored", "event": event_type, "action": action}
