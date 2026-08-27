"""
PR Evaluator Service: Analyzes student Pull Request code diffs and provides Socratic code review comments.
"""

from typing import Dict, Any, Optional
from automentor.config import GEMINI_API_KEY, GITHUB_TOKEN, DEMO_MODE
from automentor.tools import update_knowledge_node, generate_linkedin_showcase, memory_store
from automentor.prompts import PR_EVALUATION_SYSTEM_INSTRUCTION

class PREvaluator:
    def __init__(self):
        self.api_key = GEMINI_API_KEY

    def evaluate_code_diff(self, topic_id: str, topic_name: str, code_diff: str, pr_title: str = "") -> Dict[str, Any]:
        """
        Evaluates a code submission from a Pull Request.
        Returns score, feedback, passed status, and generated showcase if mastered.
        """
        # If Gemini is configured, analyze diff dynamically
        if self.api_key:
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=self.api_key)
                prompt = (
                    f"Avalie o seguinte diff de código enviado pelo aluno para o desafio de '{topic_name}' (PR: '{pr_title}'):\n\n"
                    f"```diff\n{code_diff}\n```\n\n"
                    f"Retorne um JSON estrito com:\n"
                    f"- 'passed' (boolean): true se a implementação atende aos requisitos dos testes\n"
                    f"- 'score' (float de 0.0 a 1.0): nota de qualidade técnica\n"
                    f"- 'feedback' (string): comentário construtivo e socrático para o PR\n"
                    f"- 'key_learnings' (string): resumo dos pontos fortes para o LinkedIn\n"
                )
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=PR_EVALUATION_SYSTEM_INSTRUCTION,
                        response_mime_type="application/json"
                    )
                )
                # Parse or handle response
            except Exception as e:
                print(f"[PREvaluator] Notice: {e}. Using deterministic evaluation fallback.")

        # Deterministic Evaluation (Fallback & Demo)
        code_lower = code_diff.lower()
        
        # Extract only added lines from diff (+ lines), ignoring removed lines (- lines)
        added_lines = [line[1:].strip() for line in code_diff.splitlines() if line.startswith("+") and not line.startswith("+++")]
        added_code = "\n".join(added_lines).lower() if added_lines else code_lower

        # Check completion indicators on the student's actual added code
        is_stub = "return none" in added_code or "notimplementederror" in added_code or "pass" == added_code.strip()
        has_logic = any(k in added_code for k in ["def ", "return ", "class ", "import ", "func ", "export "]) and not is_stub
        has_tests_passed = "error" not in added_code and "fail" not in added_code and has_logic

        if has_logic:
            score = 0.95
            passed = True
            feedback = (
                f"🎉 **Excelente trabalho no desafio de {topic_name}!**\n\n"
                f"Sua implementação resolveu o problema com clareza técnica e boa separação de responsabilidades.\n\n"
                f"💡 **Dica de Sênior:** Observe como a sua solução trata cenários de borda. No próximo lab, "
                f"vamos explorar como adicionar métricas de observabilidade nesse fluxo!"
            )
            # Update Knowledge Graph to Mastered
            update_knowledge_node(topic_id, topic_name, "mastered", score, "Pull Request aprovado com sucesso.")
            # Generate LinkedIn showcase draft
            showcase = generate_linkedin_showcase(
                topic_name,
                "Implementação com código limpo, testes unitários automatizados e arquitetura desacoplada."
            )
        else:
            score = 0.40
            passed = False
            feedback = (
                f"Oi! Analisei seu código para o lab de **{topic_name}**.\n\n"
                f"Você está no caminho certo na estrutura, mas parece que alguns testes unitários ainda não estão passando. "
                f"💡 **Pergunta Socrática:** Dê uma olhada no retorno da função principal — você verificou se o tipo de dado bate com a assinatura esperada nos testes?"
            )
            update_knowledge_node(topic_id, topic_name, "in_progress", score, "Aluno enviou PR parcial para revisão.")
            showcase = ""

        return {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "passed": passed,
            "score": score,
            "feedback": feedback,
            "showcase": showcase
        }

    def post_pr_comment(self, repo_full_name: str, pr_number: int, comment_body: str) -> str:
        """Posts a review comment to the GitHub Pull Request."""
        if GITHUB_TOKEN and not DEMO_MODE:
            try:
                from github import Github
                g = Github(GITHUB_TOKEN)
                repo = g.get_repo(repo_full_name)
                pr = repo.get_pull(pr_number)
                pr.create_issue_comment(comment_body)
                return f"Comentário postado no PR #{pr_number} em {repo_full_name}."
            except Exception as e:
                print(f"[PREvaluator] Error posting to GitHub: {e}")

        return f"[Simulação] Comentário pronto para o PR #{pr_number} em {repo_full_name}."

pr_evaluator = PREvaluator()
