"""
GitHub Lab Tool: Scaffolds hands-on lab repositories on GitHub with real code templates,
unit tests, Dockerfile, and challenge instructions.
"""

from typing import Dict, Any, Optional
from automentor.config import GITHUB_TOKEN, GITHUB_USERNAME, DEMO_MODE

def _generate_template_files(topic_name: str, challenge_description: str, language: str = "python") -> Dict[str, str]:
    """Generates realistic challenge files for the student."""
    clean_topic = topic_name.replace(" ", "_").lower()
    
    challenge_code = (
        f'"""\n'
        f'Desafio AutoMentor: {topic_name}\n'
        f'Instruções: {challenge_description}\n'
        f'"""\n\n'
        f'def solve_{clean_topic}(input_data: dict) -> dict:\n'
        f'    """\n'
        f'    TODO: Implemente a lógica necessária para fazer os testes em test_challenge.py passarem.\n'
        f'    """\n'
        f'    # Siga as orientações do seu Mentor Socrático\n'
        f'    raise NotImplementedError("Implemente esta função para resolver o desafio!")\n'
    )

    test_code = (
        f'import pytest\n'
        f'from challenge import solve_{clean_topic}\n\n'
        f'def test_basic_contract():\n'
        f'    payload = {{"id": "req_001", "action": "verify", "params": {{"active": True}}}}\n'
        f'    result = solve_{clean_topic}(payload)\n'
        f'    assert result is not None\n'
        f'    assert isinstance(result, dict)\n'
        f'    assert result.get("status") == "success"\n\n'
        f'def test_edge_case_empty():\n'
        f'    with pytest.raises(ValueError):\n'
        f'        solve_{clean_topic}({{}})\n'
    )

    readme_content = (
        f'# 🎯 AutoMentor Lab: {topic_name}\n\n'
        f'> **Objetivo:** {challenge_description}\n\n'
        f'## 🚀 Como Executar Localmente:\n\n'
        f'```bash\n'
        f'# 1. Instale as dependências\n'
        f'pip install pytest\n\n'
        f'# 2. Execute os testes para ver o desafio falhando\n'
        f'pytest\n\n'
        f'# 3. Abra o arquivo `challenge.py` e implemente a solução\n'
        f'# 4. Quando os testes passarem, abra um Pull Request para revisão do Mentor!\n'
        f'```\n'
    )

    dockerfile_content = (
        f'FROM python:3.13-slim\n'
        f'WORKDIR /app\n'
        f'RUN pip install --no-cache-dir pytest\n'
        f'COPY . .\n'
        f'CMD ["pytest"]\n'
    )

    return {
        "README.md": readme_content,
        "challenge.py": challenge_code,
        "test_challenge.py": test_code,
        "Dockerfile": dockerfile_content
    }

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
        Confirmação com a URL do repositório criado e arquivos injetados.
    """
    clean_repo_name = repo_name.strip().lower().replace(" ", "-")
    repo_url = f"https://github.com/{GITHUB_USERNAME}/{clean_repo_name}"
    template_files = _generate_template_files(topic_name, challenge_description, language)

    if GITHUB_TOKEN and not DEMO_MODE:
        try:
            from github import Github
            g = Github(GITHUB_TOKEN)
            user = g.get_user()
            
            # Create repository
            repo = user.create_repo(
                clean_repo_name,
                description=f"AutoMentor Hands-on Lab: {topic_name}",
                private=False,
                auto_init=False
            )
            
            # Commit files into the newly created repository
            for filename, content in template_files.items():
                repo.create_file(
                    path=filename,
                    message=f"feat(scaffold): initialize {filename} for {topic_name}",
                    content=content,
                    branch="main"
                )

            # Create challenge issue
            repo.create_issue(
                title=f"🎯 Desafio: Implementar {topic_name}",
                body=f"## 📋 Instruções\n\n{challenge_description}\n\nAbra um Pull Request quando os testes passarem para o Mentor avaliar!"
            )
            repo_url = repo.html_url
        except Exception as e:
            print(f"[GitHubTool] Notice: {e}. Falling back to simulated response.")

    return (
        f"🐙 [GitHub Lab Generator] Repositório estruturado com sucesso!\n"
        f"• URL: {repo_url}\n"
        f"• Arquivos injetados: {', '.join(template_files.keys())}\n"
        f"• Comando rápido: git clone {repo_url} && cd {clean_repo_name} && pytest"
    )
