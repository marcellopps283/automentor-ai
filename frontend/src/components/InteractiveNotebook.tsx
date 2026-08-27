"use client";

import { useState } from "react";
import Editor from "@monaco-editor/react";
import { Play, Sparkles, Bug, CheckCircle2, RotateCcw, GitBranch, Terminal, FileText, ShieldAlert } from "lucide-react";
import { HintLadder, HintTier } from "./HintLadder";

export interface NotebookCell {
  id: string;
  type: "markdown" | "code" | "test";
  title: string;
  content: string;
}

interface InteractiveNotebookProps {
  topicTitle: string;
  masteryScore: number;
  cells: NotebookCell[];
  onUpdateCell: (id: string, newContent: string) => void;
  onRunTests: (code: string) => void;
  testOutput: { passed: boolean; logs: string } | null;
  isRunningTests: boolean;
  onOpenCheatSheet: () => void;
}

const SAMPLE_HINTS: HintTier[] = [
  {
    level: 1,
    category: "Modelo Mental",
    title: "Como o Protobuf codifica chaves de dados?",
    content: "Lembre-se: O Protobuf não trafega o nome dos campos (ex: 'username') na rede. Ele usa números de tag inteiros (ex: tag_1, tag_2). O seu dicionário precisa manter esse mapeamento indexado para simular o payload binário comprimido."
  },
  {
    level: 2,
    category: "Pseudocódigo",
    title: "Estrutura da Função de Serialização",
    content: "1. Valide se user_id e username não estão vazios (caso contrário lance ValueError).\n2. Crie um dicionário com chaves 'tag_1', 'tag_2', 'tag_3' e 'status'.\n3. Retorne o dicionário completo."
  },
  {
    level: 3,
    category: "Cenário de Borda",
    title: "O que os testes em test_challenge.py esperam?",
    content: "O teste 'test_validation' passa valores vazios (None, \"\") esperando um ValueError. Certifique-se de que a validação de entrada ocorre ANTES de qualquer retorno."
  }
];

export function InteractiveNotebook({
  topicTitle,
  masteryScore,
  cells,
  onUpdateCell,
  onRunTests,
  testOutput,
  isRunningTests,
  onOpenCheatSheet
}: InteractiveNotebookProps) {
  const [activeBugLevel, setActiveBugLevel] = useState<string | null>(null);

  const codeCell = cells.find((c) => c.type === "code");
  const markdownCell = cells.find((c) => c.type === "markdown");
  const testCell = cells.find((c) => c.type === "test");

  // Calibrate Fault Injection based on student's mastery level
  const handleAdaptiveBugInjection = () => {
    if (!codeCell) return;

    let buggyCode = "";
    let levelName = "";

    if (masteryScore < 0.45) {
      levelName = "Iniciante (Validação de Tipos & Null)";
      buggyCode =
        codeCell.content +
        "\n\n# ⚠️ BUG ADAPTATIVO (Nível Iniciante): Esquecimento de checagem de nulos\n# Remova este comentário e faça a validação lançar ValueError quando user_id for None!";
    } else if (masteryScore < 0.75) {
      levelName = "Intermediário (Serialização & Formato de Schema)";
      buggyCode =
        codeCell.content +
        "\n\n# ⚠️ BUG ADAPTATIVO (Nível Intermediário): Schema Mismatch\n# O retorno está omitindo a 'tag_3' booleana, quebrando o contrato do .proto nos testes!";
    } else {
      levelName = "Avançado (Deadlock & Concorrência)";
      buggyCode =
        codeCell.content +
        "\n\n# ⚠️ BUG ADAPTATIVO (Nível Avançado): Deadlock de Canal em Concorrência\n# O canal de streaming gRPC não está sendo fechado antes do loop de saída!";
    }

    setActiveBugLevel(levelName);
    onUpdateCell(codeCell.id, buggyCode);
  };

  return (
    <div className="flex flex-col h-full bg-background overflow-y-auto">
      {/* Notebook Toolbar */}
      <div className="p-3 border-b border-border bg-card/50 flex items-center justify-between sticky top-0 z-10 backdrop-blur-md">
        <div className="flex items-center gap-2">
          <span className="text-xs px-2 py-0.5 rounded bg-blue-500/10 text-blue-500 font-mono font-bold">
            NOTEBOOK ATIVO
          </span>
          <h1 className="text-sm font-bold text-foreground truncate max-w-md">
            {topicTitle}
          </h1>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={onOpenCheatSheet}
            className="flex items-center gap-1 px-2.5 py-1.5 bg-muted hover:bg-muted/80 text-foreground text-xs font-semibold rounded-lg border border-border transition-colors"
            title="Exportar Cheat Sheet de Estudos"
          >
            <FileText size={13} className="text-blue-500" />
            <span>Guia de Bolso (.md)</span>
          </button>

          <button
            onClick={() => onRunTests(codeCell?.content || "")}
            disabled={isRunningTests}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-green-600 hover:bg-green-500 text-white font-bold rounded-lg text-xs shadow-md shadow-green-600/20 transition-all disabled:opacity-50"
          >
            <Play size={13} className="fill-current" />
            {isRunningTests ? "Executando Pytest..." : "Executar Testes (Wasm)"}
          </button>
        </div>
      </div>

      <div className="p-6 space-y-6 max-w-4xl mx-auto w-full">
        {/* Cell 1: Theory / Markdown */}
        {markdownCell && (
          <div className="bg-card border border-border rounded-xl p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between border-b border-border pb-2">
              <span className="text-[11px] font-mono font-bold text-muted-foreground uppercase flex items-center gap-1.5">
                <Sparkles size={13} className="text-blue-500" /> {markdownCell.title}
              </span>
              <span className="text-[10px] text-muted-foreground font-mono">Gerado pelo Gemini 3.5</span>
            </div>
            <div className="text-xs text-foreground/90 leading-relaxed whitespace-pre-wrap font-sans">
              {markdownCell.content}
            </div>
          </div>
        )}

        {/* Cell 2: Code Challenge (Monaco Editor) */}
        {codeCell && (
          <div className="bg-card border border-border rounded-xl overflow-hidden shadow-sm flex flex-col">
            <div className="bg-muted px-4 py-2.5 border-b border-border flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono font-bold text-foreground">
                  🐍 challenge.py
                </span>
                {activeBugLevel && (
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-yellow-500/10 text-yellow-500 border border-yellow-500/20 flex items-center gap-1">
                    <ShieldAlert size={11} /> {activeBugLevel}
                  </span>
                )}
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleAdaptiveBugInjection}
                  className="text-[11px] px-2.5 py-1 bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20 rounded-md font-semibold border border-yellow-500/20 flex items-center gap-1 transition-all"
                  title="Injeta um bug didático calibrado pelo Mentor com base no seu nível de proficiência atual"
                >
                  <Bug size={12} /> Injetar Bug Calibrado
                </button>
              </div>
            </div>

            <div className="h-64 border-b border-border">
              <Editor
                height="100%"
                defaultLanguage="python"
                value={codeCell.content}
                theme="vs-dark"
                onChange={(value) => onUpdateCell(codeCell.id, value || "")}
                options={{
                  minimap: { enabled: false },
                  fontSize: 13,
                  lineNumbers: "on",
                  scrollBeyondLastLine: false,
                  wordWrap: "on",
                  fontFamily: "JetBrains Mono, Menlo, monospace"
                }}
              />
            </div>

            {/* Progressive Hint Ladder (Under Monaco Editor) */}
            <div className="p-3 bg-muted/20 border-b border-border">
              <HintLadder hints={SAMPLE_HINTS} />
            </div>

            {/* Test Suite Viewer */}
            {testCell && (
              <div className="bg-muted/30 p-3 border-t border-border">
                <details className="text-xs text-muted-foreground">
                  <summary className="cursor-pointer font-mono font-bold text-foreground hover:text-blue-500 select-none">
                    🧪 Ver Suíte de Testes (test_challenge.py)
                  </summary>
                  <pre className="mt-2 p-3 bg-zinc-950 text-zinc-300 rounded-lg text-[11px] font-mono overflow-x-auto">
                    {testCell.content}
                  </pre>
                </details>
              </div>
            )}
          </div>
        )}

        {/* Cell 3: Test Execution Output Console */}
        {testOutput && (
          <div
            className={`border rounded-xl p-4 font-mono text-xs shadow-sm ${
              testOutput.passed
                ? "bg-green-500/5 border-green-500/30 text-green-400"
                : "bg-red-500/5 border-red-500/30 text-red-400"
            }`}
          >
            <div className="flex items-center justify-between pb-2 border-b border-current/20 font-bold">
              <span className="flex items-center gap-2">
                <Terminal size={14} />
                {testOutput.passed ? "✓ TODOS OS TESTES PASSARAM! (100% SUCESSO)" : "❌ TESTES FALHARAM (INVESTIGUE O ERRO)"}
              </span>
              <span className="text-[10px]">Pyodide Wasm Runner</span>
            </div>
            <pre className="mt-2 whitespace-pre-wrap text-[11px] leading-relaxed font-mono opacity-90">
              {testOutput.logs}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
