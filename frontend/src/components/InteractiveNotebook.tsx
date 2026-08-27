"use client";

import { useState } from "react";
import Editor from "@monaco-editor/react";
import { Play, Sparkles, Bug, CheckCircle2, RotateCcw, GitBranch, Terminal } from "lucide-react";

export interface NotebookCell {
  id: string;
  type: "markdown" | "code" | "test";
  title: string;
  content: string;
}

interface InteractiveNotebookProps {
  topicTitle: string;
  cells: NotebookCell[];
  onUpdateCell: (id: string, newContent: string) => void;
  onRunTests: (code: string) => void;
  testOutput: { passed: boolean; logs: string } | null;
  isRunningTests: boolean;
}

export function InteractiveNotebook({
  topicTitle,
  cells,
  onUpdateCell,
  onRunTests,
  testOutput,
  isRunningTests,
}: InteractiveNotebookProps) {
  const [activeTab, setActiveTab] = useState<"editor" | "tests">("editor");

  const codeCell = cells.find((c) => c.type === "code");
  const markdownCell = cells.find((c) => c.type === "markdown");
  const testCell = cells.find((c) => c.type === "test");

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
                <span className="text-[10px] text-muted-foreground">
                  (Edite o código abaixo para fazer os testes passarem)
                </span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    const buggyCode =
                      codeCell.content +
                      "\n\n# ⚠️ BUG INJETADO PELO MENTOR: Deadlock ao não fechar canal!\n# Analise o erro de concorrência nos testes.";
                    onUpdateCell(codeCell.id, buggyCode);
                  }}
                  className="text-[11px] px-2 py-1 bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20 rounded-md font-semibold border border-yellow-500/20 flex items-center gap-1"
                  title="O Mentor introduz um bug intencional para você treinar debugging"
                >
                  <Bug size={12} /> Injetar Bug Didático
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
