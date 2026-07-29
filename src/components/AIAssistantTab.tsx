import React, { useState } from "react";
import { Sparkles, Send, Bot, User, Code2, AlertCircle } from "lucide-react";

export const AIAssistantTab: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<Array<{ sender: "user" | "ai"; text: string }>>([
    {
      sender: "ai",
      text: "Hello! I am your Maple ManagementRx v2.0.0 AI Companion. How can I help you customize your Python discord.py bot or resolve deployment issues on Android?"
    }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!prompt.trim() || loading) return;

    const userText = prompt;
    setPrompt("");
    setMessages((prev) => [...prev, { sender: "user", text: userText }]);
    setLoading(true);

    try {
      const res = await fetch("/api/ai/assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userText })
      });
      const data = await res.json();
      if (data.success && data.answer) {
        setMessages((prev) => [...prev, { sender: "ai", text: data.answer }]);
      } else {
        setMessages((prev) => [
          ...prev,
          { sender: "ai", text: "Note: To enable AI assistance, please ensure your GEMINI_API_KEY environment variable is configured." }
        ]);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "Error connecting to AI service. Check your network or API key configuration." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="bg-[#151B23] rounded border border-[#2D333B] p-3.5">
        <h2 className="text-sm font-bold text-white flex items-center gap-2 font-mono">
          <Sparkles className="w-4 h-4 text-[#FF6B35]" />
          AI Development Companion & Diagnostics
        </h2>
        <p className="text-[11px] text-[#ADB5BD] mt-0.5">
          Ask questions about writing new Python discord.py cogs, configuring intents, or deploying from mobile.
        </p>
      </div>

      <div className="bg-[#0E1217] rounded border border-[#2D333B] shadow-lg flex flex-col h-[520px]">
        {/* Messages Body */}
        <div className="flex-1 p-4 overflow-y-auto space-y-3">
          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex gap-2.5 text-xs leading-relaxed ${
                m.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {m.sender === "ai" && (
                <div className="w-6 h-6 rounded bg-[#FF6B35] flex items-center justify-center text-white text-xs font-bold flex-shrink-0 shadow-sm mt-0.5">
                  M
                </div>
              )}
              <div
                className={`max-w-[85%] p-3 rounded font-mono text-[11px] whitespace-pre-wrap ${
                  m.sender === "user"
                    ? "bg-[#1A110F] text-white border border-[#FF6B35]/40 rounded-br-none"
                    : "bg-[#151B23] text-[#ADB5BD] border border-[#2D333B] rounded-bl-none"
                }`}
              >
                {m.text}
              </div>
              {m.sender === "user" && (
                <div className="w-6 h-6 rounded bg-[#2D333B] flex items-center justify-center text-white flex-shrink-0 shadow-sm mt-0.5">
                  <User className="w-3.5 h-3.5" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-xs text-[#ADB5BD] font-mono pl-8 animate-pulse">
              <Sparkles className="w-3.5 h-3.5 text-[#FF6B35]" />
              AI Companion processing query...
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="p-3 bg-[#151B23] border-t border-[#2D333B] flex items-center gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask AI how to add a custom cog or fix a bot error..."
            className="flex-1 text-xs font-mono px-3 py-2 border border-[#2D333B] rounded bg-[#0B0F13] text-white focus:outline-none focus:border-[#FF6B35]"
          />
          <button
            onClick={handleSend}
            disabled={loading || !prompt.trim()}
            className="px-3.5 py-2 bg-[#FF6B35] hover:bg-[#D44D1D] disabled:opacity-50 text-white font-mono font-bold text-xs rounded transition flex items-center gap-1.5 uppercase tracking-wider text-[11px]"
          >
            <Send className="w-3.5 h-3.5" />
            ASK
          </button>
        </div>
      </div>
    </div>
  );
};
