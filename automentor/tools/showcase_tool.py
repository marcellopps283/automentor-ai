"""
Showcase Tool: Generates technical LinkedIn articles and GitHub profile badges upon mastery.
"""

from typing import Dict, Any

def generate_linkedin_showcase(topic_name: str, key_learnings: str, repo_url: str = "") -> str:
    """
    Gera um rascunho de post de alto impacto técnico para o LinkedIn demonstrando
    a habilidade que o aluno acabou de dominar, pronta para aprovação em 1-clique.

    Args:
        topic_name: Nome da habilidade dominada (ex: 'Sistemas Distribuídos com gRPC e Protobuf').
        key_learnings: Principais decisões técnicas e aprendizados consolidados.
        repo_url: Link do repositório no GitHub para incluir no post.

    Returns:
        O rascunho formatado do post e o status de aprovação.
    """
    post_draft = (
        f"🚀 Concluindo mais uma etapa de aprendizado prático: {topic_name}!\n\n"
        f"Neste laboratório, implementei arquiteturas focadas em performance e desacoplamento:\n"
        f"💡 {key_learnings}\n\n"
        f"🔗 Repositório com a implementação e testes unitários: {repo_url or 'https://github.com/student/lab-project'}\n\n"
        f"#Backend #SoftwareEngineering #Architecture #GoogleCloud #ContinuousLearning"
    )

    return (
        f"💼 [LinkedIn Showcase] Rascunho gerado com sucesso para aprovação 1-clique:\n"
        f"────────────────────────────────────────────────────────────\n"
        f"{post_draft}\n"
        f"────────────────────────────────────────────────────────────\n"
        f"Status: Pronto para publicação via botão no Dashboard / CLI!"
    )
