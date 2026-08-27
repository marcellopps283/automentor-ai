"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Mic, MicOff, Paperclip, Calendar, GitBranch, Share2, Sparkles, Check } from "lucide-react";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  actionCard?: {
    type: "calendar" | "github" | "linkedin";
    title: string;
    details: string;
    linkUrl?: string;
  };
}

interface ChatPanelProps {
  messages: ChatMessage[];
  onSendMessage: (msg: string) => void;
  onUploadPdf: (file: File) => void;
  onOpenShowcase: (topic: string, post: string, repo: string) => void;
}

export function ChatPanel({ messages, onSendMessage, onUploadPdf, onOpenShowcase }: ChatPanelProps) {
  const [input, setInput] = useState("");
  const [isVoiceActive, setIsVoiceActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSendMessage(input);
    setInput("");
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === "application/pdf") {
      onUploadPdf(file);
    }
  };

  return (
    <div className="flex flex-col h-full bg-card border-r border-border">
      {/* Header */}
      <div className="p-3 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse" />
          <h2 className="text-xs font-bold text-foreground">Mentor Socrático</h2>
        </div>
        <button
          onClick={() => fileInputRef.current?.click()}
          className="text-xs flex items-center gap-1 text-muted-foreground hover:text-blue-500 transition-colors p-1 rounded-md"
          title="Upload de Slide / Ementa em PDF"
        >
          <Paperclip size={14} /> PDF
        </button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="application/pdf"
          className="hidden"
        />
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs leading-relaxed">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
          >
            <div
              className={`max-w-[90%] p-3 rounded-2xl ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-muted text-foreground border border-border rounded-bl-none"
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.content}</div>

              {/* Inline Action Cards */}
              {msg.actionCard && (
                <div className="mt-3 p-3 rounded-xl bg-card border border-border text-foreground space-y-2">
                  <div className="flex items-center gap-2 font-bold text-[11px]">
                    {msg.actionCard.type === "calendar" && <Calendar size={14} className="text-blue-500" />}
                    {msg.actionCard.type === "github" && <GitBranch size={14} className="text-purple-500" />}
                    {msg.actionCard.type === "linkedin" && <Share2 size={14} className="text-green-500" />}
                    <span>{msg.actionCard.title}</span>
                  </div>

                  <p className="text-[11px] text-muted-foreground">{msg.actionCard.details}</p>

                  {msg.actionCard.type === "linkedin" && (
                    <button
                      onClick={() => onOpenShowcase("gRPC & Protobuf", msg.actionCard?.details || "", msg.actionCard?.linkUrl || "")}
                      className="w-full mt-2 py-1.5 px-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg text-[10px] flex items-center justify-center gap-1.5 shadow-sm"
                    >
                      <Sparkles size={12} /> Revisar & Publicar com 1-Clique
                    </button>
                  )}

                  {msg.actionCard.linkUrl && msg.actionCard.type !== "linkedin" && (
                    <a
                      href={msg.actionCard.linkUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-block mt-1 text-[10px] text-blue-500 hover:underline font-bold"
                    >
                      Acessar link externo ↗
                    </a>
                  )}
                </div>
              )}
            </div>
            <span className="text-[9px] text-muted-foreground mt-1 px-1">{msg.timestamp}</span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Floating Animated Audio Waveform Bar (When Voice is Active) */}
      {isVoiceActive && (
        <div className="mx-4 mb-2 p-2.5 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-between text-blue-400 text-xs animate-in fade-in slide-in-from-bottom-2">
          <div className="flex items-center gap-2">
            <span className="flex gap-1 items-end h-4">
              <span className="w-1 bg-blue-500 h-2 animate-bounce" />
              <span className="w-1 bg-blue-400 h-4 animate-bounce delay-75" />
              <span className="w-1 bg-blue-600 h-3 animate-bounce delay-150" />
            </span>
            <span className="font-semibold">Ouvindo sua voz em tempo real...</span>
          </div>
          <button
            onClick={() => setIsVoiceActive(false)}
            className="text-[10px] px-2 py-1 bg-blue-600 text-white rounded-md font-bold"
          >
            Encerrar
          </button>
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-3 border-t border-border flex items-center gap-2">
        <button
          type="button"
          onClick={() => setIsVoiceActive(!isVoiceActive)}
          className={`p-2 rounded-xl border transition-all ${
            isVoiceActive
              ? "bg-red-500 text-white border-red-400 animate-pulse shadow-md shadow-red-500/20"
              : "bg-muted text-muted-foreground hover:text-foreground border-border"
          }`}
          title="Modo de Voz com Gemini Live"
        >
          {isVoiceActive ? <MicOff size={16} /> : <Mic size={16} />}
        </button>

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Tire dúvidas, responda ou diga o que quer estudar..."
          className="flex-1 bg-muted border border-border rounded-xl px-3 py-2 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-blue-500"
        />

        <button
          type="submit"
          className="p-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold shadow-md shadow-blue-500/20 transition-all"
        >
          <Send size={15} />
        </button>
      </form>
    </div>
  );
}
