"use client";

import { Network, Mic, Sparkles, AlertCircle, CheckCircle, Clock } from "lucide-react";
import { RetentionWidget } from "./RetentionWidget";

export interface KnowledgeNode {
  topic_id: string;
  topic_name: string;
  status: "mastered" | "in_progress" | "gap" | "not_started";
  mastery_score: number;
  notes?: string;
}

interface KnowledgeGraphHeaderProps {
  nodes: KnowledgeNode[];
  onOpenFullGraph: () => void;
  onOpenMockInterview: () => void;
  onScheduleReview: (topicName: string) => void;
}

export function KnowledgeGraphHeader({
  nodes,
  onOpenFullGraph,
  onOpenMockInterview,
  onScheduleReview
}: KnowledgeGraphHeaderProps) {
  const masteredCount = nodes.filter((n) => n.status === "mastered").length;
  const gapCount = nodes.filter((n) => n.status === "gap").length;

  const decayingTopics = [
    {
      topic_id: "grpc_contracts",
      topic_name: "Contratos gRPC & Protobuf",
      days_since_study: 3,
      retention_pct: 68,
      decay_risk: "medium" as const
    },
    {
      topic_id: "jwt_refresh",
      topic_name: "Autenticação JWT",
      days_since_study: 6,
      retention_pct: 42,
      decay_risk: "high" as const
    }
  ];

  return (
    <div className="bg-card border-b border-border px-4 py-2 flex items-center justify-between gap-4">
      {/* Left: Branding & Metrics */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 font-bold text-sm tracking-tight text-foreground">
          <div className="w-6 h-6 rounded-md bg-blue-600 flex items-center justify-center text-white text-xs font-black">
            AM
          </div>
          AutoMentor <span className="text-xs px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-500 font-mono font-medium">Cockpit</span>
        </div>

        <div className="h-4 w-px bg-border hidden sm:block" />

        {/* Retention Analytics Widget */}
        <RetentionWidget
          streakDays={4}
          overallRetention={84}
          decayingTopics={decayingTopics}
          onScheduleReview={onScheduleReview}
        />
      </div>

      {/* Center: Mini-Map Skill Pills */}
      <div className="hidden xl:flex items-center gap-1.5 overflow-x-auto max-w-lg py-1">
        {nodes.slice(0, 4).map((node) => {
          const pillColor = {
            mastered: "border-green-500/30 bg-green-500/10 text-green-400",
            gap: "border-red-500/30 bg-red-500/10 text-red-400",
            in_progress: "border-yellow-500/30 bg-yellow-500/10 text-yellow-400",
            not_started: "border-border bg-muted text-muted-foreground"
          }[node.status] || "border-border bg-muted text-muted-foreground";

          return (
            <div
              key={node.topic_id}
              className={`text-xs px-2.5 py-1 rounded-md border flex items-center gap-1.5 shrink-0 font-medium ${pillColor}`}
              title={`Score: ${Math.round(node.mastery_score * 100)}% | Status: ${node.status}`}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-current" />
              <span className="truncate max-w-[120px]">{node.topic_name}</span>
            </div>
          );
        })}
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        <button
          onClick={onOpenMockInterview}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold rounded-lg bg-red-500/10 text-red-500 hover:bg-red-500/20 border border-red-500/20 transition-all shadow-sm"
        >
          <Mic size={13} className="fill-current animate-pulse" />
          <span>Simular Entrevista</span>
        </button>

        <button
          onClick={onOpenFullGraph}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-muted text-foreground hover:bg-muted/80 border border-border transition-all shadow-sm"
        >
          <Network size={14} className="text-blue-500" />
          <span className="hidden sm:inline">Explorar</span> Grafo 2D
        </button>
      </div>
    </div>
  );
}
