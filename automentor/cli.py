"""
AutoMentor CLI: Interactive terminal interface for the student to chat with their AI Mentor.
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt
from automentor.mentor_core import mentor_brain
from automentor.tools import memory_store

console = Console()

def print_banner():
    banner_text = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║   🎓 AutoMentor AI — Seu Companheiro de Estudos Autônomo          ║
    ║   Gemini 2.0 • Google ADK • Calendar • GitHub • Knowledge Graph   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    console.print(f"[bold cyan]{banner_text}[/bold cyan]")
    console.print("[dim]Comandos especiais: digite [bold]/graph[/bold] para ver suas habilidades ou [bold]/exit[/bold] para sair.[/dim]\n")

def display_knowledge_graph():
    topics = memory_store.get_all_topics()
    if not topics:
        console.print("[yellow]Nenhum tópico registrado no Knowledge Graph ainda. Comece conversando com o Mentor![/yellow]\n")
        return

    table = Table(title="🧠 Seu Knowledge Graph de Habilidades", show_header=True, header_style="bold magenta")
    table.add_column("Tópico", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Score", justify="center")
    table.add_column("Última Atualização", style="dim")

    for node in topics:
        status = node.get("status", "not_started")
        score = node.get("mastery_score", 0.0)
        
        status_display = {
            "mastered": "[bold green]✓ DOMINADO[/bold green]",
            "in_progress": "[bold yellow]⏳ EM ESTUDO[/bold yellow]",
            "gap": "[bold red]⚠ LACUNA DETECTADA[/bold red]",
            "not_started": "[dim]NÃO INICIADO[/dim]"
        }.get(status, status)

        score_bar = f"{int(score * 100)}%"

        table.add_row(
            node.get("topic_name", node.get("topic_id")),
            status_display,
            score_bar,
            node.get("last_updated", "-")[:19].replace("T", " ")
        )

    console.print(table)
    console.print()

def start_cli():
    print_banner()
    mentor_brain.start_session()

    # Welcome message
    welcome_msg = (
        "Fala Marcelo! Sou o **AutoMentor**, seu companheiro de estudos.\n\n"
        "O que você precisa dominar agora? É uma matéria da faculdade, uma prova chegando, "
        "ou uma habilidade que você quer colocar no currículo? Me conta!"
    )
    console.print(Panel(Markdown(welcome_msg), title="[bold cyan]AutoMentor[/bold cyan]", border_style="cyan"))

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]Você[/bold green]")
            if not user_input.strip():
                continue

            if user_input.strip().lower() in ("/exit", "exit", "sair", "quit"):
                console.print("\n[cyan]Bons estudos e até a próxima sessão! 👋[/cyan]\n")
                break

            if user_input.strip().lower() in ("/graph", "graph", "/grafo", "grafo"):
                display_knowledge_graph()
                continue

            with console.status("[bold cyan]O Mentor está analisando e preparando ações...[/bold cyan]"):
                response = mentor_brain.send_message(user_input)

            reply = response.get("reply", "")
            console.print(Panel(Markdown(reply), title="[bold cyan]AutoMentor[/bold cyan]", border_style="cyan"))

        except (KeyboardInterrupt, EOFError):
            console.print("\n[cyan]Sessão finalizada. Até logo![/cyan]")
            break

if __name__ == "__main__":
    start_cli()
