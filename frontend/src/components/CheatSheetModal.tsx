"use client";

import { useState } from "react";
import { Download, Copy, Check, Printer, X, FileText, Sparkles } from "lucide-react";

interface CheatSheetModalProps {
  isOpen: boolean;
  onClose: () => void;
  topicTitle: string;
  markdownContent: string;
}

export function CheatSheetModal({
  isOpen,
  onClose,
  topicTitle,
  markdownContent
}: CheatSheetModalProps) {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(markdownContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([markdownContent], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `CheatSheet_${topicTitle.replace(/\s+/g, "_")}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-md flex items-center justify-center p-6">
      <div className="bg-card border border-border rounded-2xl max-w-3xl w-full h-[85vh] flex flex-col justify-between p-6 shadow-2xl animate-in fade-in zoom-in duration-200">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border pb-4">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-blue-500/10 text-blue-500">
              <FileText size={20} />
            </div>
            <div>
              <h3 className="text-base font-bold text-foreground">
                📄 Guia de Bolso & Cheat Sheet: {topicTitle}
              </h3>
              <p className="text-xs text-muted-foreground">
                Resumo executivo com modelos mentais, código resolvido e pegadinhas de prova.
              </p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 rounded-lg bg-muted text-muted-foreground hover:text-foreground">
            <X size={18} />
          </button>
        </div>

        {/* Content Viewer */}
        <div className="flex-1 overflow-y-auto my-4 p-5 bg-muted/30 border border-border rounded-xl font-mono text-xs text-foreground/90 whitespace-pre-wrap leading-relaxed">
          {markdownContent}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between border-t border-border pt-4">
          <span className="text-[11px] text-muted-foreground font-sans">
            Compatível com Notion, Obsidian e visualizadores Markdown.
          </span>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-lg bg-muted text-foreground hover:bg-muted/80 border border-border transition-all"
            >
              {copied ? <Check size={14} className="text-green-500" /> : <Copy size={14} />}
              <span>{copied ? "Copiado!" : "Copiar Texto"}</span>
            </button>

            <button
              onClick={handleDownload}
              className="flex items-center gap-1.5 px-4 py-2 text-xs font-bold rounded-lg bg-blue-600 hover:bg-blue-500 text-white shadow-md shadow-blue-500/20 transition-all"
            >
              <Download size={14} />
              <span>Baixar Arquivo .MD</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
