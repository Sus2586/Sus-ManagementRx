import React, { useState } from "react";
import { ShieldCheck, Cpu, Server, Key, RefreshCw, CheckCircle2, AlertCircle, Copy, Check, Power, ExternalLink, Zap } from "lucide-react";

export const DashboardTab: React.FC = () => {
  const [copied, setCopied] = useState(false);
  const [botStatus, setBotStatus] = useState<"online" | "idle" | "stopped">("online");
  const [tokenInput, setTokenInput] = useState("**************************");
  const [tokenSaved, setTokenSaved] = useState(false);

  const handleCopyEnv = () => {
    const envContent = `BOT_TOKEN=your_copied_discord_bot_token\nBOT_NAME=Maple ManagementRx\nBOT_VERSION=2.0.0\nDEVELOPER=Maple Dev Team\nEMBED_COLOR=0xFF6B35\nLOG_LEVEL=DEBUG`;
    navigator.clipboard.writeText(envContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4">
      {/* Bot Status Top Bar */}
      <div className="bg-[#151B23] rounded border border-[#2D333B] p-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded bg-gradient-to-br from-[#FF6B35] to-[#D44D1D] flex items-center justify-center text-white text-lg font-bold shadow-sm">
            M
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-bold text-white tracking-tight">Maple ManagementRx</h2>
              <span className="text-[10px] font-mono text-[#FF6B35] bg-[#1A110F] px-1.5 py-0.5 rounded border border-[#FF6B35]/30">
                v2.0.0
              </span>
            </div>
            <p className="text-[11px] text-[#ADB5BD] opacity-70">
              Production-Ready Discord Management Engine • Zero-PC Architecture
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-2.5 py-1 bg-[#0B0F13] border border-[#2D333B] rounded text-[10px] font-mono">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            <span className="text-green-400 font-semibold">
              {botStatus === "online" ? "SYSTEM OPERATIONAL" : "SYSTEM IDLE"}
            </span>
          </div>
          <button
            onClick={() => setBotStatus(botStatus === "online" ? "idle" : "online")}
            className="px-3 py-1.5 rounded bg-[#FF6B35] hover:bg-[#D44D1D] text-white text-xs font-bold transition flex items-center gap-1.5 uppercase tracking-wider text-[10px]"
          >
            <Power className="w-3.5 h-3.5" />
            {botStatus === "online" ? "Restart Engine" : "Start Bot"}
          </button>
        </div>
      </div>

      {/* 4-Column High Density Metric Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <div className="bg-[#151B23] p-3.5 rounded border border-[#2D333B]">
          <div className="text-[10px] font-bold uppercase opacity-60 mb-1 tracking-wider">Total Guilds</div>
          <div className="text-2xl font-mono text-white font-bold">1,284</div>
          <div className="text-[10px] text-green-400 mt-1 font-mono">+12 Since Yesterday</div>
        </div>

        <div className="bg-[#151B23] p-3.5 rounded border border-[#2D333B]">
          <div className="text-[10px] font-bold uppercase opacity-60 mb-1 tracking-wider">Active Users</div>
          <div className="text-2xl font-mono text-white font-bold">482.5k</div>
          <div className="text-[10px] text-blue-400 mt-1 font-mono">8.2k Concurrent</div>
        </div>

        <div className="bg-[#151B23] p-3.5 rounded border border-[#2D333B]">
          <div className="text-[10px] font-bold uppercase opacity-60 mb-1 tracking-wider">Latency / Shard Ping</div>
          <div className="text-2xl font-mono text-white font-bold flex items-center gap-1.5">
            <Zap className="w-4 h-4 text-[#FF6B35]" />
            34 ms
          </div>
          <div className="text-[10px] text-green-400 mt-1 font-mono">Heartbeat OK (Shard #1)</div>
        </div>

        <div className="bg-[#151B23] p-3.5 rounded border border-[#2D333B]">
          <div className="text-[10px] font-bold uppercase opacity-60 mb-1 tracking-wider">Mod Actions</div>
          <div className="text-2xl font-mono text-white font-bold">12,094</div>
          <div className="text-[10px] text-orange-400 mt-1 font-mono">324 Active Strikes</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Environment & Secret Manager */}
        <div className="lg:col-span-7 bg-[#0E1217] rounded border border-[#2D333B] p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-[#2D333B] pb-2.5">
            <div className="flex items-center gap-2">
              <Key className="w-4 h-4 text-[#FF6B35]" />
              <h3 className="font-bold text-xs uppercase text-white tracking-widest font-mono">
                Secrets & Environment Configuration
              </h3>
            </div>
            <button
              onClick={handleCopyEnv}
              className="text-[10px] font-mono px-2.5 py-1 rounded border border-[#2D333B] bg-[#151B23] hover:bg-[#2D333B] text-white flex items-center gap-1 transition"
            >
              {copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}
              {copied ? "COPIED" : "COPY .ENV"}
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-[11px] font-mono text-[#ADB5BD] mb-1">
                Discord Bot Token (`BOT_TOKEN`)
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="password"
                  value={tokenInput}
                  onChange={(e) => setTokenInput(e.target.value)}
                  placeholder="Paste your Discord Bot Token..."
                  className="flex-1 text-xs font-mono px-3 py-1.5 border border-[#2D333B] rounded bg-[#0B0F13] text-white focus:outline-none focus:border-[#FF6B35]"
                />
                <button
                  onClick={() => {
                    setTokenSaved(true);
                    setTimeout(() => setTokenSaved(false), 2000);
                  }}
                  className="px-3 py-1.5 text-xs font-mono font-bold bg-[#FF6B35] hover:bg-[#D44D1D] text-white rounded transition"
                >
                  {tokenSaved ? "SAVED" : "SAVE"}
                </button>
              </div>
              <span className="text-[10px] font-mono text-amber-400/80 mt-1 block">
                🔐 Store securely. Never expose tokens in public repositories.
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 pt-1">
              <div>
                <label className="block text-[11px] font-mono text-[#ADB5BD] mb-1">
                  Embed Accent (`EMBED_COLOR`)
                </label>
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded bg-[#FF6B35] border border-white/20 flex-shrink-0"></div>
                  <input
                    type="text"
                    readOnly
                    value="0xFF6B35 (Flame Orange)"
                    className="w-full text-[11px] font-mono px-2.5 py-1 border border-[#2D333B] rounded bg-[#0B0F13] text-white"
                  />
                </div>
              </div>

              <div>
                <label className="block text-[11px] font-mono text-[#ADB5BD] mb-1">
                  Database URL
                </label>
                <input
                  type="text"
                  readOnly
                  value="sqlite:///database/maple.db"
                  className="w-full text-[11px] font-mono px-2.5 py-1 border border-[#2D333B] rounded bg-[#0B0F13] text-white"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Infrastructure & System Health Panel */}
        <div className="lg:col-span-5 bg-[#0E1217] rounded border border-[#2D333B] p-4 flex flex-col justify-between space-y-3">
          <h3 className="text-[10px] font-bold text-white uppercase tracking-widest font-mono border-b border-[#2D333B] pb-2">
            Infrastructure Health
          </h3>
          <div className="space-y-3">
            <div className="flex flex-col gap-1">
              <div className="flex justify-between text-[11px] font-mono">
                <span>CPU Usage (Container)</span>
                <span className="text-white">12.4%</span>
              </div>
              <div className="h-1.5 w-full bg-[#2D333B] rounded-full overflow-hidden">
                <div className="h-full bg-green-500 w-[12.4%]"></div>
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <div className="flex justify-between text-[11px] font-mono">
                <span>Memory Allocation</span>
                <span className="text-white">124 MB / 512 MB</span>
              </div>
              <div className="h-1.5 w-full bg-[#2D333B] rounded-full overflow-hidden">
                <div className="h-full bg-orange-500 w-[24%]"></div>
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <div className="flex justify-between text-[11px] font-mono">
                <span>SQLite DB Connections</span>
                <span className="text-green-400">aiosqlite Active</span>
              </div>
              <div className="h-1.5 w-full bg-[#2D333B] rounded-full overflow-hidden">
                <div className="h-full bg-green-500 w-[8%]"></div>
              </div>
            </div>
          </div>

          <div className="p-2.5 bg-[#151B23] border border-[#2D333B] rounded text-center">
            <div className="text-[10px] font-mono uppercase text-[#ADB5BD]">Bot API Latency</div>
            <div className="text-xl font-mono font-bold text-green-400 mt-0.5">34 ms</div>
          </div>
        </div>
      </div>

      {/* Module Health Monitor & Feature Status */}
      <div className="bg-[#0E1217] rounded border border-[#2D333B] p-4 space-y-3">
        <div className="flex items-center justify-between border-b border-[#2D333B] pb-2">
          <h3 className="text-[10px] font-bold text-white uppercase tracking-widest font-mono">
            Module Health Monitor
          </h3>
          <span className="text-[9px] font-mono px-2 py-0.5 bg-green-500/10 text-green-400 border border-green-500/30 rounded uppercase">
            6/6 Modules Active
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
          {[
            { title: "WKB_ESCALATION", desc: "Warn, Kick, Ban & Automatic Escalation", status: "Operational" },
            { title: "TICKET_SYSTEM", desc: "Persistent UI Panels & HTML Transcripts", status: "Operational" },
            { title: "APP_ENGINE", desc: "Modal Forms & Reviewer Approvals", status: "Operational" },
            { title: "MOD_LOGGER", desc: "Deletes, Edits, Joins & Role Audits", status: "Operational" },
            { title: "GUILD_CONFIG", desc: "Multi-Server Isolated Settings", status: "Operational" },
            { title: "STRIKE_PERSIST", desc: "Async SQLite DB Storage", status: "Operational" }
          ].map((item, idx) => (
            <div key={idx} className="p-2.5 border border-[#2D333B] bg-[#151B23] rounded flex items-center justify-between">
              <div>
                <div className="text-[11px] font-mono font-bold text-white">{item.title}</div>
                <div className="text-[10px] text-[#ADB5BD] opacity-70 mt-0.5">{item.desc}</div>
              </div>
              <div className="px-2 py-0.5 bg-green-500/10 text-green-400 text-[9px] border border-green-500/30 rounded font-mono uppercase whitespace-nowrap">
                {item.status}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
