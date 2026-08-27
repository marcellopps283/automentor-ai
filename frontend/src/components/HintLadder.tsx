"use client";

import { useState } from "react";
import { Lightbulb, ChevronDown, ChevronUp, Lock, Unlock, HelpCircle } from "lucide-react";

export interface HintTier {
  level: 1 | 2 | 3;
  title: string;
  category: "Modelo Mental" | "Pseudocódigo" | "Cenário de Borda";
  content: string;
}

interface HintLadderProps {
  hints: HintTier[];
}

export function HintLadder({ hints }: HintLadderProps) {
  const [unlockedLevel, setUnlockedLevel] = useState<number>(0);
  const [openLevel, setOpenLevel] = useState<number | null>(null);

  const handleUnlockNext = (level: number) => {
    if (level > unlockedLevel) {
      setUnlockedLevel(level);
    }
    setOpenLevel(openLevel === level ? null : level);
  };

  return (
    <div className="bg-card border border-border rounded-xl p-4 shadow-sm space-y-3">
      <div className="flex items-center justify-between border-b border-border pb-2">
        <div className="flex items-center gap-2">
          <Lightbulb size={16} className="text-yellow-500" />
          <h3 className="text-xs font-bold text-foreground">
            Dicas em 3 Camadas (Progressive Hint Ladder)
          </h3>
        </div>
        <span className="text-[10px] text-muted-foreground font-mono">
          {unlockedLevel}/3 Dicas Desbloqueadas
        </span>
      </div>

      <p className="text-[11px] text-muted-foreground leading-relaxed">
        Travou no desafio? Desbloqueie dicas graduais sem estragar o aprendizado ativo:
      </p>

      <div className="space-y-2">
        {hints.map((hint) => {
          const isUnlocked = hint.level <= unlockedLevel;
          const isOpen = openLevel === hint.level;

          return (
            <div
              key={hint.level}
              className={`border rounded-lg transition-all ${
                isUnlocked
                  ? "bg-muted/50 border-border"
                  : "bg-muted/20 border-dashed border-border/70 opacity-80"
              }`}
            >
              <button
                onClick={() => handleUnlockNext(hint.level)}
                className="w-full px-3 py-2 flex items-center justify-between text-left text-xs font-semibold text-foreground hover:text-blue-500 transition-colors"
              >
                <div className="flex items-center gap-2">
                  {isUnlocked ? (
                    <Unlock size={13} className="text-green-500 shrink-0" />
                  ) : (
                    <Lock size={13} className="text-muted-foreground shrink-0" />
                  )}
                  <span className="font-mono text-[10px] uppercase px-1.5 py-0.5 rounded bg-card border border-border text-muted-foreground">
                    Nível {hint.level}: {hint.category}
                  </span>
                  <span className="truncate">{hint.title}</span>
                </div>
                {isOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
              </button>

              {isUnlocked && isOpen && (
                <div className="px-3 pb-3 pt-1 text-xs text-foreground/90 font-sans leading-relaxed border-t border-border/40 mt-1 whitespace-pre-wrap animate-in fade-in duration-150">
                  {hint.content}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
