"""
Mentor Core: The central brain orchestrating the Socratic dialog and tool execution via Gemini.
"""

from typing import List, Dict, Any, Optional
from automentor.config import GEMINI_API_KEY
from automentor.prompts import MENTOR_SYSTEM_INSTRUCTION
from automentor.tools import MENTOR_TOOLS, memory_store

class MentorBrain:
    def __init__(self, model_name: str = "gemini-3.5-flash"):
        self.model_name = model_name
        self.api_key = GEMINI_API_KEY
        self.client = None
        self.chat_session = None
        self.history: List[Dict[str, str]] = []
        
        self._init_client()

    def _init_client(self):
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[MentorBrain] Notice: Google GenAI client init: {e}")
                self.client = None

    def start_session(self):
        """Initializes or resets a conversation session with the Mentor."""
        self.history = []
        if self.client:
            try:
                from google.genai import types
                config = types.GenerateContentConfig(
                    system_instruction=MENTOR_SYSTEM_INSTRUCTION,
                    tools=MENTOR_TOOLS,
                    temperature=0.7,
                )
                self.chat_session = self.client.chats.create(
                    model=self.model_name,
                    config=config
                )
            except Exception as e:
                print(f"[MentorBrain] Error creating chat session: {e}")
                self.chat_session = None

    def send_message(self, user_input: str) -> Dict[str, Any]:
        """
        Sends a message from the student to the Mentor and processes responses + tool calls.
        Returns a dict containing the text response and any tools executed.
        """
        self.history.append({"role": "user", "content": user_input})
        executed_tools = []

        # 1. Real Gemini Client Execution (if available)
        if self.client and self.chat_session:
            try:
                response = self.chat_session.send_message(user_input)
                
                # Check for automatic function calls and tool results
                text_parts = []
                if hasattr(response, "text") and response.text:
                    text_parts.append(response.text)

                reply_text = "\n".join(text_parts) if text_parts else "Entendido! Vamos em frente."
                self.history.append({"role": "assistant", "content": reply_text})
                return {
                    "reply": reply_text,
                    "tools_executed": executed_tools,
                    "mode": "live_gemini"
                }
            except Exception as e:
                print(f"[MentorBrain] Gemini API call error: {e}. Utilizing local fallback.")

        # 2. Local Fallback Socratic Simulation (for zero-config local testing)
        reply, tools = self._local_socratic_fallback(user_input)
        self.history.append({"role": "assistant", "content": reply})
        return {
            "reply": reply,
            "tools_executed": tools,
            "mode": "simulation"
        }

    def _local_socratic_fallback(self, user_input: str) -> tuple[str, list]:
        """
        Provides realistic Socratic dialog and proactive tool triggers for testing.
        """
        user_lower = user_input.lower()
        tools_run = []

        # Check for mastery explanation first
        if any(k in user_lower for k in ["tag", "varint", "parsing", "overhead", "binário"]) and any(k in user_lower for k in ["json", "protobuf", "serializa", "texto"]):
            from automentor.tools import update_knowledge_node, generate_linkedin_showcase
            res_node = update_knowledge_node("grpc_contracts", "Contratos gRPC & Protobuf", "mastered", 0.95, "Conceito dominado com clareza técnica.")
            res_show = generate_linkedin_showcase("Sistemas Distribuídos com gRPC & Protobuf", "Serialização binária eficiente, definição de contratos estritos e benchmarking com REST.")
            tools_run.extend([res_node, res_show])

            reply = (
                "Perfeito! Você acertou em cheio no ponto central: o JSON exige parsing de texto caractere por caractere em runtime, "
                "enquanto o Protobuf serializa os campos em binário indexados por números de tag (tags numéricas fixas), eliminando overhead.\n\n"
                "🎉 **Habilidade Consolidada!** Atualizei seu score de proficiência para **95% (Mastered)** no seu Knowledge Graph.\n\n"
                "Já gerei uma sugestão de post técnico para o seu LinkedIn documentando esse seu lab prático. Quer dar uma olhada e aprovar?"
            )
            return reply, tools_run

        elif "grpc" in user_lower or "protobuf" in user_lower or "distribuídos" in user_lower or "prova" in user_lower:
            from automentor.tools import update_knowledge_node, schedule_study_session, create_github_lab
            
            # Execute the triad of autonomous tools
            res_node = update_knowledge_node("grpc_contracts", "Contratos gRPC & Protobuf", "gap", 0.4, "Aluno está iniciando e precisa fixar tipagem binária.")
            res_cal = schedule_study_session("Prática de Contratos Protobuf com gRPC", duration_minutes=30, suggested_day_offset=1)
            res_lab = create_github_lab("lab-grpc-protobuf-contracts", "gRPC & Protocol Buffers", "Definir contrato .proto, gerar stubs e passar testes unitários de serialização.", "python")
            
            tools_run.extend([res_node, res_cal, res_lab])

            reply = (
                "Excelente escolha! gRPC e Protobuf são a espinha dorsal de microsserviços modernos de altíssima performance.\n\n"
                "Para calibrarmos nosso ponto de partida de forma prática:\n"
                "💡 **Pergunta do Mentor:** Quando você compara uma API REST trafegando JSON com gRPC trafegando Protocol Buffers, "
                "por que o Protobuf consegue ser até 5x a 10x mais rápido em serialização e economizar tanta largura de banda?\n\n"
                "*(Enquanto você pensa, já me adiantei no background para você economizar tempo:)*\n"
                f"• {res_node}\n"
                f"• {res_cal.splitlines()[0]} ({res_cal.splitlines()[2]})\n"
                f"• {res_lab.splitlines()[0]} ({res_lab.splitlines()[1]})\n\n"
                "Quando estiver pronto, me conta sua resposta ou clona o repo para começarmos!"
            )
            return reply, tools_run

        else:
            reply = (
                f"Olá! Sou seu Mentor de Estudos. Vamos descomplicar esse tema juntos.\n\n"
                "Me conta: qual matéria da faculdade ou tecnologia você gostaria de praticar hoje? "
                "(Ex: *gRPC, Docker, Concorrência em Go, Autenticação JWT, Kubernetes...*)"
            )
            return reply, tools_run

mentor_brain = MentorBrain()
