"use client";

import { useState } from "react";
import { Network, Sparkles, AlertCircle, CheckCircle, Clock } from "lucide-react";

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
}

export function KnowledgeGraphHeader({ nodes, onOpenFullGraph }: KnowledgeGraphHeaderProps) {
  const masteredCount = nodes.filter(n => n.status === "mastered").length;
  const gapCount = nodes.filter(n => n.status === "gap").length;

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

        {/* Live Mastery Capsule */}
        <div className="hidden md:flex items-center gap-2 text-xs">
          <span className="flex items-center gap-1 text-green-500 font-medium bg-green-500/10 px-2 py-0.5 rounded-full">
            <CheckCircle size={12} /> {masteredCount} Dominados
          </span>
          {gapCount > 0 && (
            <span className="flex items-center gap-1 text-red-500 font-medium bg-red-500/10 px-2 py-0.5 rounded-full">
              <AlertCircle size={12} /> {gapCount} Lacuna{gapCount > 1 ? "s" : ""}
            </span>
          )}
        </div>
      </div>

      {/* Center: Mini-Map Skill Pills */}
      <div className="hidden lg:flex items-center gap-1.5 overflow-x-auto max-w-xl py-1">
        {nodes.slice(0, 5).map((node) => {
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

      {/* Right: Full Graph Button */}
      <button
        onClick={onOpenFullGraph}
        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-muted text-foreground hover:bg-muted/80 border border-border transition-all shadow-sm"
      >
        <Network size={14} className="text-blue-500" />
        <span className="hidden sm:inline">Explorar</span> Grafo 2D
      </button>
    </div>
  );
}
