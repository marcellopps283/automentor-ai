"use client";

import { useEffect } from "react";
import confetti from "canvas-confetti";
import { CheckCircle2, Share2, X, ExternalLink } from "lucide-react";

interface ShowcaseModalProps {
  isOpen: boolean;
  onClose: () => void;
  topicName: string;
  postContent: string;
  repoUrl: string;
}

export function ShowcaseModal({ isOpen, onClose, topicName, postContent, repoUrl }: ShowcaseModalProps) {
  useEffect(() => {
    if (isOpen) {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-card border border-border rounded-xl max-w-xl w-full p-6 shadow-2xl animate-in fade-in zoom-in duration-200">
        <div className="flex items-center justify-between pb-4 border-b border-border">
          <div className="flex items-center gap-2 text-green-500">
            <CheckCircle2 size={24} />
            <h3 className="text-lg font-bold text-foreground">Habilidade 100% Consolidada!</h3>
          </div>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground">
            <X size={20} />
          </button>
        </div>

        <div className="mt-4 space-y-4">
          <p className="text-sm text-muted-foreground">
            Parabéns! Você concluiu o lab de <strong className="text-foreground">{topicName}</strong>. O AutoMentor preparou seu rascunho de vitrine profissional para comprovar suas habilidades técnicas:
          </p>

          <div className="bg-muted p-4 rounded-lg border border-border font-sans text-xs whitespace-pre-wrap text-foreground leading-relaxed">
            {postContent}
          </div>

          <div className="flex items-center justify-between pt-2">
            <a
              href={repoUrl || "https://github.com"}
              target="_blank"
              rel="noreferrer"
              className="text-xs text-blue-500 hover:underline flex items-center gap-1"
            >
              Ver repositório no GitHub <ExternalLink size={12} />
            </a>

            <div className="flex gap-2">
              <button
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-muted text-muted-foreground hover:text-foreground transition-colors"
              >
                Mais Tarde
              </button>
              <button
                onClick={() => {
                  alert("🎉 Publicação enviada com sucesso para o LinkedIn!");
                  onClose();
                }}
                className="px-4 py-2 text-xs font-bold rounded-lg bg-blue-600 hover:bg-blue-500 text-white flex items-center gap-1.5 shadow-md shadow-blue-500/20"
              >
                <Share2 size={14} /> Publicar no LinkedIn
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
