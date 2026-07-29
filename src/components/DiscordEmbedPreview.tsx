import React from "react";
import { Bot, CheckCircle2, AlertTriangle, XCircle, Shield, ExternalLink } from "lucide-react";

interface EmbedField {
  name: string;
  value: string;
  inline?: boolean;
}

interface EmbedButton {
  label: string;
  style: "primary" | "secondary" | "success" | "danger";
  emoji?: string;
}

interface EmbedData {
  title?: string;
  description?: string;
  color?: string;
  fields?: EmbedField[];
  footer?: string;
  timestamp?: string;
  interactiveButtons?: EmbedButton[];
}

export const DiscordEmbedPreview: React.FC<{ embed: EmbedData }> = ({ embed }) => {
  const borderLeftColor = embed.color || "#FF6B35";

  return (
    <div className="bg-[#151B23] text-gray-100 rounded p-4 font-mono shadow-lg border border-[#2D333B]">
      {/* Discord Bot Header */}
      <div className="flex items-center gap-2 mb-3 border-b border-[#2D333B] pb-2">
        <div className="w-7 h-7 rounded bg-gradient-to-br from-[#FF6B35] to-[#D44D1D] flex items-center justify-center text-white font-bold text-xs shadow-sm">
          M
        </div>
        <div>
          <div className="flex items-center gap-1.5">
            <span className="font-semibold text-xs text-white">Maple ManagementRx</span>
            <span className="bg-[#5865F2] text-[9px] text-white font-bold px-1 py-0.2 rounded tracking-wide">
              BOT
            </span>
          </div>
          <span className="text-[10px] text-gray-400">Today at 6:25 PM</span>
        </div>
      </div>

      {/* Embed Container */}
      <div
        className="bg-[#0B0F13] rounded p-3 text-xs shadow-inner border-y border-r border-[#2D333B]"
        style={{ borderLeft: `4px solid ${borderLeftColor}` }}
      >
        {/* Title */}
        {embed.title && (
          <h4 className="font-bold text-base text-white mb-1.5 flex items-center gap-1.5">
            {embed.title}
          </h4>
        )}

        {/* Description */}
        {embed.description && (
          <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed mb-3">
            {embed.description}
          </p>
        )}

        {/* Fields */}
        {embed.fields && embed.fields.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 my-3 border-t border-[#3f4147] pt-2">
            {embed.fields.map((f, i) => (
              <div key={i} className={f.inline ? "col-span-1" : "col-span-full"}>
                <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                  {f.name}
                </div>
                <div className="text-sm text-gray-200 mt-0.5 font-medium whitespace-pre-line">
                  {f.value}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Footer */}
        {embed.footer && (
          <div className="text-[11px] text-gray-400 border-t border-[#3f4147] pt-2 mt-2 flex items-center justify-between">
            <span>{embed.footer}</span>
            {embed.timestamp && (
              <span>{new Date(embed.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            )}
          </div>
        )}
      </div>

      {/* Interactive Action Components (Buttons) */}
      {embed.interactiveButtons && embed.interactiveButtons.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-3 pt-2">
          {embed.interactiveButtons.map((btn, i) => (
            <button
              key={i}
              className={`px-3 py-1.5 rounded text-xs font-semibold flex items-center gap-1.5 transition ${
                btn.style === "primary"
                  ? "bg-[#5865F2] hover:bg-[#4752C4] text-white"
                  : btn.style === "success"
                  ? "bg-[#248046] hover:bg-[#1a6334] text-white"
                  : btn.style === "danger"
                  ? "bg-[#da373c] hover:bg-[#a1282c] text-white"
                  : "bg-[#4e5058] hover:bg-[#6d6f78] text-white"
              }`}
            >
              {btn.emoji && <span>{btn.emoji}</span>}
              <span>{btn.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
