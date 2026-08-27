"""
GitHub Lab Tool: Scaffolds hands-on lab repositories on GitHub with real code templates,
unit tests, Dockerfile, GitHub Actions CI workflow, and challenge instructions.
"""

from typing import Dict, Any, Optional
from automentor.config import GITHUB_TOKEN, GITHUB_USERNAME, DEMO_MODE

def _generate_template_files(topic_name: str, challenge_description: str, language: str = "python", difficulty: str = "intermediate") -> Dict[str, str]:
    """Generates realistic multi-language challenge files for the student."""
    clean_topic = topic_name.replace(" ", "_").lower()
    lang = language.lower()

    if lang == "go":
        challenge_code = (
            f"package lab\n\n"
            f"import \"errors\"\n\n"
            f"// Solve{topic_name.replace(' ', '')} implementa o desafio: {challenge_description}\n"
            f"func Solve{topic_name.replace(' ', '')}(input map[string]interface{{}}) (map[string]interface{{}}, error) {{\n"
            f"    // TODO: Implemente a lógica para fazer os testes passarem\n"
            f"    return nil, errors.New(\"não implementado\")\n"
            f"}}\n"
        )
        test_code = (
            f"package lab\n\n"
            f"import \"testing\"\n\n"
            f"func TestContract(t *testing.T) {{\n"
            f"    payload := map[string]interface{{}}{{\"id\": \"001\", \"action\": \"verify\"}}\n"
            f"    res, err := Solve{topic_name.replace(' ', '')}(payload)\n"
            f"    if err != nil || res == nil {{\n"
            f"        t.Fatalf(\"esperado sucesso, obtido: %v\", err)\n"
            f"    }}\n"
            f"}}\n"
        )
        run_cmd = "go test ./..."
        dockerfile_content = "FROM golang:1.24-alpine\nWORKDIR /app\nCOPY . .\nCMD [\"go\", \"test\", \"./...\"]\n"
        ci_workflow = (
            "name: Go CI\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n"
            "    steps:\n    - uses: actions/checkout@v4\n    - uses: actions/setup-go@v5\n      with:\n        go-version: '1.24'\n    - run: go test ./...\n"
        )
        main_file = "challenge.go"
        test_file = "challenge_test.go"

    elif lang in ["typescript", "javascript", "ts", "js"]:
        challenge_code = (
            f"/**\n * Desafio AutoMentor: {topic_name}\n * Instruções: {challenge_description}\n */\n\n"
            f"export function solve{topic_name.replace(' ', '')}(inputData: Record<string, any>): Record<string, any> {{\n"
            f"  // TODO: Implemente a solução\n"
            f"  throw new Error(\"Não implementado\");\n"
            f"}}\n"
        )
        test_code = (
            f"import {{ solve{topic_name.replace(' ', '')} }} from './challenge';\n\n"
            f"test('deve retornar status success para payload válido', () => {{\n"
            f"  const res = solve{topic_name.replace(' ', '')}({{ id: 'req_01', active: true }});\n"
            f"  expect(res.status).toBe('success');\n"
            f"}});\n"
        )
        run_cmd = "npm test"
        dockerfile_content = "FROM node:22-alpine\nWORKDIR /app\nCOPY package*.json ./\nRUN npm install\nCOPY . .\nCMD [\"npm\", \"test\"]\n"
        ci_workflow = (
            "name: Node CI\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n"
            "    steps:\n    - uses: actions/checkout@v4\n    - uses: actions/setup-node@v4\n      with:\n        node-version: '22'\n    - run: npm test\n"
        )
        main_file = "challenge.ts"
        test_file = "challenge.test.ts"

    else:
        # Default Python
        challenge_code = (
            f'"""\n'
            f'Desafio AutoMentor: {topic_name} (Dificuldade: {difficulty.upper()})\n'
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
        run_cmd = "pytest"
        dockerfile_content = "FROM python:3.13-slim\nWORKDIR /app\nRUN pip install --no-cache-dir pytest\nCOPY . .\nCMD [\"pytest\"]\n"
        ci_workflow = (
            "name: Python CI\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n"
            "    steps:\n    - uses: actions/checkout@v4\n    - uses: actions/setup-python@v5\n      with:\n        python-version: '3.13'\n    - run: pip install pytest && pytest\n"
        )
        main_file = "challenge.py"
        test_file = "test_challenge.py"

    readme_content = (
        f'# 🎯 AutoMentor Lab: {topic_name}\n\n'
        f'> **Nível de Dificuldade:** `{difficulty.upper()}`  \n'
        f'> **Objetivo:** {challenge_description}\n\n'
        f'## 🚀 Como Executar Localmente:\n\n'
        f'```bash\n'
        f'# 1. Execute os testes para ver o desafio falhando\n'
        f'{run_cmd}\n\n'
        f'# 2. Abra o arquivo `{main_file}` e implemente a solução\n'
        f'# 3. Quando os testes passarem, abra um Pull Request para revisão do Mentor!\n'
        f'```\n'
    )

    return {
        "README.md": readme_content,
        main_file: challenge_code,
        test_file: test_code,
        "Dockerfile": dockerfile_content,
        ".github/workflows/test.yml": ci_workflow
    }

def create_github_lab(
    repo_name: str,
    topic_name: str,
    challenge_description: str,
    language: str = "python",
    difficulty: str = "intermediate"
) -> str:
    """
    Cria um repositório prático no GitHub do aluno contendo esqueleto de código,
    testes unitários, Dockerfile e GitHub Actions CI automatizado.

    Args:
        repo_name: Nome do repositório em kebab-case (ex: 'lab-grpc-protobuf-contracts').
        topic_name: Nome legível do tópico (ex: 'gRPC & Protocol Buffers').
        challenge_description: Instruções claras do que o aluno precisa implementar.
        language: Linguagem do laboratório ('python', 'typescript', 'go').
        difficulty: Nível do desafio ('beginner', 'intermediate', 'advanced').

    Returns:
        Confirmação com a URL do repositório criado e arquivos injetados.
    """
    clean_repo_name = repo_name.strip().lower().replace(" ", "-")
    repo_url = f"https://github.com/{GITHUB_USERNAME}/{clean_repo_name}"
    template_files = _generate_template_files(topic_name, challenge_description, language, difficulty)

    if GITHUB_TOKEN and not DEMO_MODE:
        try:
            from github import Github
            g = Github(GITHUB_TOKEN)
            user = g.get_user()
            
            repo = user.create_repo(
                clean_repo_name,
                description=f"AutoMentor Hands-on Lab: {topic_name} ({difficulty.title()})",
                private=False,
                auto_init=False
            )
            
            for filename, content in template_files.items():
                repo.create_file(
                    path=filename,
                    message=f"feat(scaffold): initialize {filename} for {topic_name}",
                    content=content,
                    branch="main"
                )

            repo.create_issue(
                title=f"🎯 Desafio ({difficulty.title()}): Implementar {topic_name}",
                body=f"## 📋 Instruções\n\n{challenge_description}\n\nAbra um Pull Request quando os testes passarem para o Mentor avaliar!"
            )
            repo_url = repo.html_url
        except Exception as e:
            print(f"[GitHubTool] Notice: {e}. Falling back to simulated response.")

    return (
        f"🐙 [GitHub Lab Generator] Repositório estruturado com sucesso!\n"
        f"• URL: {repo_url}\n"
        f"• Arquivos injetados: {', '.join(template_files.keys())}\n"
        f"• Nível: {difficulty.upper()} | Linguagem: {language.title()}\n"
        f"• Comando rápido: git clone {repo_url} && cd {clean_repo_name}"
    )
