"""
Showcase Tool: Generates technical LinkedIn articles, GitHub profile badges, and resume bullet points.
"""

from typing import Dict, Any, Optional

def generate_linkedin_showcase(
    topic_name: str,
    key_learnings: str,
    repo_url: str = "",
    format_type: str = "linkedin_post"
) -> str:
    """
    Gera material de vitrine profissional (post de LinkedIn, badge para o README do GitHub
    ou bullet point para o currículo) demonstrando a habilidade técnica que o aluno dominou.

    Args:
        topic_name: Nome da habilidade dominada (ex: 'Sistemas Distribuídos com gRPC e Protobuf').
        key_learnings: Principais decisões técnicas, arquiteturais e métricas de aprendizado.
        repo_url: Link do repositório no GitHub para inclusão no post/badge.
        format_type: Formato desejado ('linkedin_post', 'github_badge', 'resume_bullet', 'all').

    Returns:
        O material formatado pronto para uso profissional em 1-clique.
    """
    clean_repo = repo_url or "https://github.com/student/lab-project"
    badge_url = f"https://img.shields.io/badge/AutoMentor_Certified-{topic_name.replace(' ', '_')}-2ea44f?style=for-the-badge&logo=googlecloud"

    post_draft = (
        f"🚀 Concluindo mais uma etapa de aprendizado prático: **{topic_name}**!\n\n"
        f"Neste laboratório, implementei arquiteturas com foco em alta performance e desacoplamento:\n"
        f"💡 {key_learnings}\n\n"
        f"🔗 Repositório com testes unitários e Dockerfile: {clean_repo}\n\n"
        f"#Backend #SoftwareEngineering #Architecture #GoogleCloud #Gemini #AllThingsAgentic"
    )

    resume_bullet = f"• Desenvolveu serviços em {topic_name} com testes unitários automatizados e containerização Docker ({clean_repo})."
    github_badge = f"[![{topic_name}]({badge_url})]({clean_repo})"

    if format_type == "resume_bullet":
        output = f"📋 [Currículo / Resume Bullet Point]:\n{resume_bullet}"
    elif format_type == "github_badge":
        output = f"🛡️ [Badge Markdown para o GitHub Profile]:\n{github_badge}"
    elif format_type == "all":
        output = (
            f"💼 [Pacote Completo de Vitrine]:\n"
            f"1. Post do LinkedIn:\n{post_draft}\n\n"
            f"2. Markdown Badge:\n{github_badge}\n\n"
            f"3. Bullet Point para CV:\n{resume_bullet}"
        )
    else:
        output = (
            f"💼 [LinkedIn Showcase] Rascunho gerado com sucesso para aprovação 1-clique:\n"
            f"────────────────────────────────────────────────────────────\n"
            f"{post_draft}\n"
            f"────────────────────────────────────────────────────────────\n"
            f"Status: Pronto para publicação via botão no Dashboard / CLI!"
        )

    return output
