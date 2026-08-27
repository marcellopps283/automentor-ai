"""
Cheat Sheet Tool: Generates structured, high-yield study guides and exam cheat sheets.
"""

from typing import List, Optional

def generate_study_cheat_sheet(
    topic_name: str,
    core_principles: str,
    common_pitfalls: str,
    code_example: str = ""
) -> str:
    """
    Gera um Guia de Bolso / Cheat Sheet executivo para revisão rápida antes de provas ou entrevistas técnicas.

    Args:
        topic_name: Nome do tópico de estudo (ex: 'Sistemas Distribuídos: Contratos gRPC & Protobuf').
        core_principles: Os 2 a 4 princípios conceituais e arquiteturais mais importantes.
        common_pitfalls: Armadilhas clássicas em provas, pegadinhas de código e erros comuns.
        code_example: Snippet de código modelo ou contrato de exemplo.

    Returns:
        O Guia de Bolso completo formatado em Markdown limpo.
    """
    cheat_sheet = (
        f"# 📄 Guia de Bolso: {topic_name}\n"
        f"> Compilado pelo **AutoMentor AI** para retenção máxima e revisão pré-prova.\n\n"
        f"## 🎯 1. Modelos Mentais & Conceitos Centrais\n"
        f"{core_principles}\n\n"
        f"## ⚠️ 2. Pegadinhas Clássicas & Armadilhas em Provas\n"
        f"{common_pitfalls}\n\n"
    )

    if code_example:
        cheat_sheet += (
            f"## 💻 3. Snippet de Referência / Contrato\n"
            f"```python\n"
            f"{code_example.strip()}\n"
            f"```\n"
        )

    return cheat_sheet
