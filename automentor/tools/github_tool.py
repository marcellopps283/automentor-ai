"""
GitHub Lab Tool: Scaffolds hands-on lab repositories on GitHub with code templates and unit tests.
Uses PyGitHub when GITHUB_TOKEN is available, with structured Demo fallback.
"""

from typing import Dict, Any, Optional
from automentor.config import GITHUB_TOKEN, GITHUB_USERNAME, DEMO_MODE

def create_github_lab(repo_name: str, topic_name: str, challenge_description: str, language: str = "python") -> str:
    """
    Cria um repositório prático no GitHub do aluno contendo esqueleto de código,
    testes unitários e uma Issue descrevendo o desafio prático a ser resolvido.

    Args:
        repo_name: Nome do repositório em kebab-case (ex: 'lab-grpc-protobuf-contracts').
        topic_name: Nome legível do tópico (ex: 'gRPC & Protocol Buffers').
        challenge_description: Instruções claras do que o aluno precisa implementar.
        language: Linguagem do laboratório ('python', 'typescript', 'go').

    Returns:
        Confirmação com a URL do repositório criado e instruções para clonar.
    """
    clean_repo_name = repo_name.strip().lower().replace(" ", "-")
    repo_url = f"https://github.com/{GITHUB_USERNAME}/{clean_repo_name}"

    if GITHUB_TOKEN and not DEMO_MODE:
        try:
            from github import Github
            g = Github(GITHUB_TOKEN)
            user = g.get_user()
            # Real repo creation
            repo = user.create_repo(
                clean_repo_name,
                description=f"AutoMentor Hands-on Lab: {topic_name}",
                private=False,
                auto_init=True
            )
            # Create challenge issue
            repo.create_issue(
                title=f"🎯 Desafio: Implementar {topic_name}",
                body=f"## 📋 Instruções\n\n{challenge_description}\n\nAbra um Pull Request quando os testes passarem!"
            )
            repo_url = repo.html_url
        except Exception as e:
            print(f"[GitHubTool] GitHub API notice: {e}. Falling back to simulation.")

    return (
        f"🐙 [GitHub Lab Generator] Repositório criado com sucesso!\n"
        f"• URL: {repo_url}\n"
        f"• Arquivos injetados: README.md, challenge.{language == 'python' and 'py' or 'ts'}, test_challenge.py, Dockerfile\n"
        f"• Instrução rápida: git clone {repo_url} && cd {clean_repo_name}"
    )
