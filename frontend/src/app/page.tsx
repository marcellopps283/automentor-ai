"use client";

import { useState } from "react";
import { KnowledgeGraphHeader, KnowledgeNode } from "@/components/KnowledgeGraphHeader";
import { KnowledgeGraphModal } from "@/components/KnowledgeGraphModal";
import { ChatPanel, ChatMessage } from "@/components/ChatPanel";
import { InteractiveNotebook, NotebookCell } from "@/components/InteractiveNotebook";
import { ShowcaseModal } from "@/components/ShowcaseModal";
import { ThemeToggle } from "@/components/ThemeToggle";

const INITIAL_NODES: KnowledgeNode[] = [
  {
    topic_id: "grpc_contracts",
    topic_name: "Contratos gRPC & Protobuf",
    status: "in_progress",
    mastery_score: 0.4,
    notes: "Praticando definição de esquemas .proto e serialização binária."
  },
  {
    topic_id: "rest_architecture",
    topic_name: "Arquitetura REST e HTTP/2",
    status: "mastered",
    mastery_score: 1.0,
    notes: "Dominado com sucesso: verbos HTTP, status codes e idempotência."
  },
  {
    topic_id: "jwt_refresh",
    topic_name: "Autenticação JWT & Refresh Tokens",
    status: "gap",
    mastery_score: 0.25,
    notes: "Lacuna: confusão entre tempo de expiração do access token vs rotação de refresh token."
  },
  {
    topic_id: "docker_microservices",
    topic_name: "Containerização com Docker",
    status: "in_progress",
    mastery_score: 0.6,
    notes: "Configuração de multi-stage builds e isolamento de redes."
  }
];

const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: "m_1",
    role: "assistant",
    content: "Fala Marcelo! Sou seu **AutoMentor**. Vamos descomplicar seus estudos!\n\nVi que você está estudando **Sistemas Distribuídos com gRPC e Protobuf**. Já preparei seu **Notebook Interativo** na direita com o código esqueleto e os testes unitários prontos.",
    timestamp: "Agora",
    actionCard: {
      type: "calendar",
      title: "Google Calendar Bloqueado",
      details: "Sessão prática agendada para amanhã às 18h30 (30 min livres)",
      linkUrl: "https://calendar.google.com"
    }
  },
  {
    id: "m_2",
    role: "assistant",
    content: "💡 **Pergunta Socrática:** Por que no Protocol Buffers nós usamos tags numéricas (ex: `int32 id = 1;`) em vez de nomes de variáveis como no JSON?",
    timestamp: "Agora"
  }
];

const INITIAL_CELLS: NotebookCell[] = [
  {
    id: "cell_theory",
    type: "markdown",
    title: "1. Teoria & Mental Model: Por que Protobuf?",
    content: "### 💡 O Conceito Central\nAo contrário do JSON que envia as strings das chaves repetidamente a cada requisição (ex: `\"user_id\": 123`), o **Protocol Buffers** codifica os campos em formato binário comprimido usando tags numéricas fixas.\n\n```mermaid\nflowchart LR\n  JSON[\"JSON Payload (142 bytes)\"] -->|Parsing de Texto em Runtime| REST[\"REST Server\"]\n  PROTO[\"Protobuf Binário (28 bytes)\"] -->|Indexação por Tag Direta| GRPC[\"gRPC Server\"]\n```"
  },
  {
    id: "cell_code",
    type: "code",
    title: "2. Desafio Prático",
    content: `def serialize_user_payload(user_id: int, username: str, is_active: bool) -> dict:
    """
    Serializa os dados do usuário simulando o payload comprimido do Protobuf.
    Retorna o dicionário serializado contendo status 'success'.
    """
    if not user_id or not username:
        raise ValueError("Dados de usuário inválidos")

    # TODO: Complete a serialização simulada para passar nos testes
    return {
        "tag_1": user_id,
        "tag_2": username,
        "tag_3": is_active,
        "status": "success"
    }
`
  },
  {
    id: "cell_test",
    type: "test",
    title: "3. Suíte de Testes (test_challenge.py)",
    content: `def test_serialization():
    payload = serialize_user_payload(101, "marcelo", True)
    assert payload["status"] == "success"
    assert payload["tag_1"] == 101

def test_validation():
    try:
        serialize_user_payload(None, "", False)
        assert False, "Deveria lançar ValueError"
    except ValueError:
        pass
`
  }
];

export default function CockpitPage() {
  const [nodes, setNodes] = useState<KnowledgeNode[]>(INITIAL_NODES);
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [cells, setCells] = useState<NotebookCell[]>(INITIAL_CELLS);
  
  const [isGraphModalOpen, setIsGraphModalOpen] = useState(false);
  const [showcaseData, setShowcaseData] = useState<{ isOpen: boolean; topic: string; post: string; repo: string }>({
    isOpen: false,
    topic: "",
    post: "",
    repo: ""
  });

  const [testOutput, setTestOutput] = useState<{ passed: boolean; logs: string } | null>(null);
  const [isRunningTests, setIsRunningTests] = useState(false);

  const handleSendMessage = async (msg: string) => {
    const userMsg: ChatMessage = {
      id: `u_${Date.now()}`,
      role: "user",
      content: msg,
      timestamp: "Agora"
    };
    setMessages((prev) => [...prev, userMsg]);

    // Check if user is answering or asking
    const lower = msg.toLowerCase();
    setTimeout(() => {
      let replyContent = "Interessante ponto de vista! Observe como isso se reflete diretamente na performance de rede do seu microserviço.";
      let card = undefined;

      if (lower.includes("tag") || lower.includes("número") || lower.includes("binário") || lower.includes("tamanho")) {
        replyContent = "🎉 **Exato!** As tags numéricas funcionam como ponteiros indexados diretamente em C++/Rust, eliminando o overhead de string matching do JSON.\n\nAtualizei seu Knowledge Graph para **Mastered (100%)**!";
        
        // Update knowledge graph
        setNodes((prev) =>
          prev.map((n) =>
            n.topic_id === "grpc_contracts"
              ? { ...n, status: "mastered", mastery_score: 1.0, notes: "Conceito dominado com clareza técnica." }
              : n
          )
        );

        card = {
          type: "linkedin" as const,
          title: "Showcase Profissional Pronto",
          details: "Rascunho de post do LinkedIn com resumo técnico e links do repositório pronto para publicação.",
          linkUrl: "https://github.com/student/lab-grpc"
        };
      }

      setMessages((prev) => [
        ...prev,
        {
          id: `a_${Date.now()}`,
          role: "assistant",
          content: replyContent,
          timestamp: "Agora",
          actionCard: card
        }
      ]);
    }, 600);
  };

  const handleUploadPdf = (file: File) => {
    setMessages((prev) => [
      ...prev,
      {
        id: `u_${Date.now()}`,
        role: "user",
        content: `📄 Upload do arquivo: ${file.name}`,
        timestamp: "Agora"
      },
      {
        id: `a_${Date.now()}`,
        role: "assistant",
        content: `✓ **${file.name} processado pelo Gemini 3.5!**\nExtraí 4 tópicos principais e atualizei seu Knowledge Graph com os pré-requisitos identificados.`,
        timestamp: "Agora"
      }
    ]);
  };

  const handleUpdateCell = (id: string, newContent: string) => {
    setCells((prev) => prev.map((c) => (c.id === id ? { ...c, content: newContent } : c)));
  };

  const handleRunTests = (code: string) => {
    setIsRunningTests(true);
    setTestOutput(null);

    setTimeout(() => {
      setIsRunningTests(false);
      const isBuggy = code.includes("BUG INJETADO");
      
      if (isBuggy) {
        setTestOutput({
          passed: false,
          logs: `============================= FAILURES =============================\n__________________________ test_serialization __________________________\nE   DeadlockError: Channel never closed before consumer loop exit.\nE   AssertionError: assert False\n=========================== 1 failed in 0.04s ===========================`
        });
      } else {
        setTestOutput({
          passed: true,
          logs: `============================= test session starts =============================\nplatform wasm32 -- Python 3.13 (Pyodide)\ncollected 2 items\n\ntest_challenge.py ..                                                      [100%]\n============================== 2 passed in 0.03s ==============================`
        });
      }
    }, 800);
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-background text-foreground">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-border bg-card">
        <div className="flex-1">
          <KnowledgeGraphHeader
            nodes={nodes}
            onOpenFullGraph={() => setIsGraphModalOpen(true)}
          />
        </div>
        <div className="px-4 py-2 border-l border-border flex items-center gap-2">
          <ThemeToggle />
        </div>
      </div>

      {/* Main Cockpit Split-Screen */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left: Socratic Chat (35% width) */}
        <div className="w-[35%] min-w-[340px] max-w-[500px] h-full">
          <ChatPanel
            messages={messages}
            onSendMessage={handleSendMessage}
            onUploadPdf={handleUploadPdf}
            onOpenShowcase={(topic, post, repo) =>
              setShowcaseData({ isOpen: true, topic, post, repo })
            }
          />
        </div>

        {/* Right: Autonomous Interactive Notebook (65% width) */}
        <div className="flex-1 h-full">
          <InteractiveNotebook
            topicTitle="Sistemas Distribuídos: Contratos e Tipagem com gRPC & Protobuf"
            cells={cells}
            onUpdateCell={handleUpdateCell}
            onRunTests={handleRunTests}
            testOutput={testOutput}
            isRunningTests={isRunningTests}
          />
        </div>
      </div>

      {/* Modals */}
      <KnowledgeGraphModal
        isOpen={isGraphModalOpen}
        onClose={() => setIsGraphModalOpen(false)}
        nodes={nodes}
      />

      <ShowcaseModal
        isOpen={showcaseData.isOpen}
        onClose={() => setShowcaseData({ ...showcaseData, isOpen: false })}
        topicName={showcaseData.topic}
        postContent={showcaseData.post}
        repoUrl={showcaseData.repo}
      />
    </div>
  );
}
