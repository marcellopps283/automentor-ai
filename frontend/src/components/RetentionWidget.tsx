"use client";

import { useState } from "react";
import { Flame, Clock, Calendar, CheckCircle2, ChevronRight, X, Sparkles } from "lucide-react";

interface RetentionItem {
  topic_id: string;
  topic_name: string;
  days_since_study: number;
  retention_pct: number;
  decay_risk: "high" | "medium" | "low";
}

interface RetentionWidgetProps {
  streakDays: number;
  overallRetention: number;
  decayingTopics: RetentionItem[];
  onScheduleReview: (topicName: string) => void;
}

export function RetentionWidget({
  streakDays,
  overallRetention,
  decayingTopics,
  onScheduleReview
}: RetentionWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      {/* Header Badges */}
      <div className="flex items-center gap-2">
        {/* Daily Streak */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-orange-500/10 text-orange-500 hover:bg-orange-500/20 border border-orange-500/20 text-xs font-bold transition-all"
          title="Ofensiva de Estudos Diários"
        >
          <Flame size={14} className="fill-current animate-pulse" />
          <span>{streakDays} Dias</span>
        </button>

        {/* Ebbinghaus Retention Score */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-500 hover:bg-blue-500/20 border border-blue-500/20 text-xs font-bold transition-all"
          title="Saúde da Memória (Curva de Ebbinghaus)"
        >
          <Clock size={14} />
          <span>{overallRetention}% Retenção</span>
        </button>
      </div>

      {/* Popover */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-card border border-border rounded-xl shadow-2xl p-4 z-50 animate-in fade-in zoom-in-95 duration-150">
          <div className="flex items-center justify-between pb-3 border-b border-border">
            <div className="flex items-center gap-1.5 font-bold text-xs text-foreground">
              <Sparkles size={14} className="text-blue-500" />
              <span>Saúde da Memória (Ebbinghaus)</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-muted-foreground hover:text-foreground">
              <X size={16} />
            </button>
          </div>

          <p className="text-[11px] text-muted-foreground mt-2 leading-relaxed">
            Algoritmo de Repetição Espaçada calculando o declínio de memória em <strong>D+1, D+3, D+7 e D+14</strong>:
          </p>

          <div className="mt-3 space-y-2 max-h-60 overflow-y-auto">
            {decayingTopics.map((item) => (
              <div
                key={item.topic_id}
                className="bg-muted/40 border border-border rounded-lg p-2.5 flex flex-col gap-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-foreground truncate max-w-[170px]">
                    {item.topic_name}
                  </span>
                  <span
                    className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${
                      item.decay_risk === "high"
                        ? "bg-red-500/10 text-red-500 border border-red-500/20"
                        : "bg-yellow-500/10 text-yellow-500 border border-yellow-500/20"
                    }`}
                  >
                    {item.retention_pct}%
                  </span>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <span className="text-[10px] text-muted-foreground">
                    Estudado há {item.days_since_study} dias
                  </span>
                  <button
                    onClick={() => {
                      onScheduleReview(item.topic_name);
                      setIsOpen(false);
                    }}
                    className="text-[10px] text-blue-500 hover:text-blue-400 font-bold flex items-center gap-1 bg-blue-500/10 px-2 py-0.5 rounded"
                  >
                    <Calendar size={11} /> Agendar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
