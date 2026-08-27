"use client";

import { useState, useEffect } from "react";
import { Mic, MicOff, PhoneOff, Award, Sparkles, CheckCircle2, AlertCircle, RefreshCw } from "lucide-react";

interface MockInterviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  topicName: string;
}

export function MockInterviewModal({ isOpen, onClose, topicName }: MockInterviewModalProps) {
  const [seconds, setSeconds] = useState(0);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [isFinished, setIsFinished] = useState(false);
  const [userTranscript, setUserTranscript] = useState("");

  const interviewQuestions = [
    {
      q: `Olá! Sou seu Tech Lead avaliador. Vamos começar: No contexto de ${topicName}, como você explicaria a diferença arquitetural e o impacto de throughput entre uma chamada RPC síncrona e uma fila de eventos assíncrona?`,
      hint: "Foque em latência, acoplamento temporal e resiliência a picos de carga."
    },
    {
      q: "Excelente. E como você lidaria com a garantia de entrega e idempotência caso a rede sofra uma partição transitória no meio de uma transação?",
      hint: "Mencione chaves de idempotência (Idempotency Keys) e retries exponenciais com jitter."
    },
    {
      q: "Para fecharmos: Como você monitoraria a saúde dessa infraestrutura em produção no Google Cloud?",
      hint: "Mencione Cloud Monitoring, métricas de p99 latency e tracing distribuído com OpenTelemetry."
    }
  ];

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isOpen && !isFinished) {
      interval = setInterval(() => setSeconds((s) => s + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [isOpen, isFinished]);

  if (!isOpen) return null;

  const formatTimer = (secs: number) => {
    const mins = Math.floor(secs / 60);
    const rem = secs % 60;
    return `${mins.toString().padStart(2, "0")}:${rem.toString().padStart(2, "0")}`;
  };

  const handleNextQuestion = () => {
    if (currentStep < interviewQuestions.length - 1) {
      setCurrentStep(currentStep + 1);
      setUserTranscript("");
    } else {
      setIsFinished(true);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/90 backdrop-blur-xl flex items-center justify-center p-6">
      <div className="bg-zinc-950 border border-zinc-800 rounded-3xl max-w-3xl w-full h-[85vh] flex flex-col justify-between p-8 shadow-2xl text-white">
        {/* Top Header */}
        <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse" />
            <div>
              <h2 className="text-sm font-bold tracking-wide uppercase text-zinc-300">
                Simulação de Entrevista Técnica (Google Meet Call)
              </h2>
              <span className="text-xs text-zinc-500 font-mono">
                Vaga: Backend & Distributed Systems Engineer • {topicName}
              </span>
            </div>
          </div>

          <div className="px-3 py-1 rounded-full bg-zinc-900 border border-zinc-700 font-mono text-xs font-bold text-zinc-300">
            ⏱️ {formatTimer(seconds)}
          </div>
        </div>

        {/* Center Stage */}
        {!isFinished ? (
          <div className="flex-1 flex flex-col items-center justify-center my-6 space-y-6 text-center max-w-xl mx-auto">
            {/* Tech Lead Avatar & Pulse */}
            <div className="relative">
              <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-3xl font-black shadow-2xl shadow-blue-500/30">
                🎓
              </div>
              <span className="absolute -bottom-2 -right-2 px-2 py-0.5 rounded-full bg-green-500 text-black text-[9px] font-bold">
                Ao Vivo
              </span>
            </div>

            {/* Question Text */}
            <div className="space-y-3">
              <span className="text-xs font-mono font-bold text-blue-400 uppercase tracking-wider">
                Pergunta {currentStep + 1} de {interviewQuestions.length}
              </span>
              <h3 className="text-base sm:text-lg font-semibold text-zinc-100 leading-relaxed">
                "{interviewQuestions[currentStep].q}"
              </h3>
              <p className="text-xs text-zinc-500 italic">
                💡 Dica do Mentor: {interviewQuestions[currentStep].hint}
              </p>
            </div>

            {/* Audio Waveform Simulator */}
            <div className="flex items-center justify-center gap-1.5 h-10 w-full">
              {[40, 70, 90, 60, 100, 45, 80, 65, 95, 30, 85].map((h, i) => (
                <span
                  key={i}
                  className="w-1.5 bg-blue-500 rounded-full animate-bounce"
                  style={{
                    height: `${h}%`,
                    animationDelay: `${i * 100}ms`
                  }}
                />
              ))}
            </div>

            <p className="text-xs text-zinc-400">
              Ouvindo sua resposta por voz... Fale com clareza defendendo seu raciocínio.
            </p>
          </div>
        ) : (
          /* Scorecard Screen */
          <div className="flex-1 flex flex-col justify-center my-4 space-y-5 animate-in fade-in zoom-in duration-200 max-w-xl mx-auto w-full">
            <div className="text-center space-y-1">
              <div className="inline-flex p-3 rounded-full bg-green-500/10 text-green-400 border border-green-500/20 mb-2">
                <Award size={32} />
              </div>
              <h3 className="text-xl font-bold text-white">Scorecard de Desempenho Técnico</h3>
              <p className="text-xs text-zinc-400">Resultado da avaliação gerado pelo Gemini 3.5 Flash</p>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
                <span className="text-xs font-bold text-zinc-400 uppercase">Veredito da Banca:</span>
                <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 font-mono font-bold text-xs border border-green-500/30">
                  STRONG HIRE (Aprovado com Louvor)
                </span>
              </div>

              <div className="grid grid-cols-3 gap-3 text-center">
                <div className="p-3 bg-zinc-950 rounded-xl border border-zinc-800">
                  <div className="text-xl font-mono font-bold text-blue-400">92/100</div>
                  <div className="text-[10px] text-zinc-500 mt-0.5">Fundamentos de Arquitetura</div>
                </div>
                <div className="p-3 bg-zinc-950 rounded-xl border border-zinc-800">
                  <div className="text-xl font-mono font-bold text-green-400">95/100</div>
                  <div className="text-[10px] text-zinc-500 mt-0.5">Clareza & Comunicação</div>
                </div>
                <div className="p-3 bg-zinc-950 rounded-xl border border-zinc-800">
                  <div className="text-xl font-mono font-bold text-purple-400">88/100</div>
                  <div className="text-[10px] text-zinc-500 mt-0.5">Tratamento de Falhas</div>
                </div>
              </div>

              <div className="space-y-2 text-xs text-zinc-300">
                <div className="flex items-start gap-2">
                  <CheckCircle2 size={15} className="text-green-500 shrink-0 mt-0.5" />
                  <span><strong>Ponto Forte:</strong> Domínio claro de serialização binária e isolamento de contratos em gRPC.</span>
                </div>
                <div className="flex items-start gap-2">
                  <Sparkles size={15} className="text-yellow-500 shrink-0 mt-0.5" />
                  <span><strong>Oportunidade:</strong> Explorar mais métricas de observabilidade distribuída com OpenTelemetry no Cloud Run.</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Bottom Call Controls */}
        <div className="flex items-center justify-between border-t border-zinc-800 pt-4">
          <button
            onClick={() => {
              setIsFinished(false);
              setCurrentStep(0);
              setSeconds(0);
              onClose();
            }}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 text-xs font-semibold transition-colors"
          >
            <PhoneOff size={16} className="text-red-400" />
            <span>Encerrar Chamada</span>
          </button>

          {!isFinished ? (
            <button
              onClick={handleNextQuestion}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-lg shadow-blue-600/30 transition-all"
            >
              <span>{currentStep === interviewQuestions.length - 1 ? "Finalizar & Gerar Scorecard" : "Próxima Pergunta →"}</span>
            </button>
          ) : (
            <button
              onClick={onClose}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-green-600 hover:bg-green-500 text-white text-xs font-bold transition-all"
            >
              <span>Salvar no Histórico & Fechar</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
