"use client";

import { X, CheckCircle, AlertCircle, Clock } from "lucide-react";
import { KnowledgeNode } from "./KnowledgeGraphHeader";

interface KnowledgeGraphModalProps {
  isOpen: boolean;
  onClose: () => void;
  nodes: KnowledgeNode[];
}

export function KnowledgeGraphModal({ isOpen, onClose, nodes }: KnowledgeGraphModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-md flex items-center justify-center p-6">
      <div className="bg-card border border-border rounded-2xl max-w-4xl w-full h-[80vh] flex flex-col p-6 shadow-2xl animate-in fade-in zoom-in duration-200">
        <div className="flex items-center justify-between pb-4 border-b border-border">
          <div>
            <h3 className="text-xl font-bold text-foreground">🧠 Seu Grafo de Conhecimento & Competências</h3>
            <p className="text-xs text-muted-foreground">Mapeamento em tempo real gerenciado pelo Gemini 3.5 e Google Cloud Firestore</p>
          </div>
          <button onClick={onClose} className="p-2 rounded-lg bg-muted text-muted-foreground hover:text-foreground">
            <X size={20} />
          </button>
        </div>

        {/* 2D Visual Map Grid */}
        <div className="flex-1 overflow-y-auto py-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {nodes.map((node) => {
            const statusConfig = {
              mastered: {
                label: "Dominado (Mastered)",
                color: "text-green-500 bg-green-500/10 border-green-500/30",
                icon: CheckCircle
              },
              gap: {
                label: "Lacuna Detectada",
                color: "text-red-500 bg-red-500/10 border-red-500/30",
                icon: AlertCircle
              },
              in_progress: {
                label: "Em Estudo",
                color: "text-yellow-500 bg-yellow-500/10 border-yellow-500/30",
                icon: Clock
              },
              not_started: {
                label: "Não Iniciado",
                color: "text-zinc-400 bg-zinc-500/10 border-zinc-500/20",
                icon: Clock
              }
            }[node.status] || {
              label: node.status,
              color: "text-zinc-400 bg-zinc-500/10 border-zinc-500/20",
              icon: Clock
            };

            const Icon = statusConfig.icon;

            return (
              <div
                key={node.topic_id}
                className="bg-muted/40 border border-border rounded-xl p-4 flex flex-col justify-between hover:border-blue-500/50 transition-all group"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border flex items-center gap-1 ${statusConfig.color}`}>
                      <Icon size={10} /> {statusConfig.label}
                    </span>
                    <span className="text-xs font-mono font-bold text-foreground">
                      {Math.round(node.mastery_score * 100)}%
                    </span>
                  </div>

                  <h4 className="font-bold text-sm text-foreground group-hover:text-blue-400 transition-colors">
                    {node.topic_name}
                  </h4>
                  {node.notes && (
                    <p className="text-xs text-muted-foreground mt-2 line-clamp-3 leading-relaxed">
                      💡 {node.notes}
                    </p>
                  )}
                </div>

                <div className="mt-4 pt-3 border-t border-border/50 flex items-center justify-between text-[11px] text-muted-foreground font-mono">
                  <span>ID: {node.topic_id}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
