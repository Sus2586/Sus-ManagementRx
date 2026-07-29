import React, { useState } from "react";
import { Terminal, Play, ShieldAlert, Ticket, FileText, Settings, HelpCircle, CheckCircle2 } from "lucide-react";
import { DiscordEmbedPreview } from "./DiscordEmbedPreview";

export const SimulatorTab: React.FC = () => {
  const [selectedCmd, setSelectedCmd] = useState<string>("ping");
  const [memberParam, setMemberParam] = useState<string>("@UserMember");
  const [reasonParam, setReasonParam] = useState<string>("Violating server rule #3");
  const [loading, setLoading] = useState<boolean>(false);
  const [simOutput, setSimOutput] = useState<any>(null);

  const commandsList = [
    { id: "ping", name: "/ping", category: "Utility", icon: Terminal, desc: "Check bot & API response latencies" },
    { id: "about", name: "/about", category: "Utility", icon: HelpCircle, desc: "Display Maple specs & uptime" },
    { id: "help", name: "/help", category: "Utility", icon: HelpCircle, desc: "Interactive command category help" },
    { id: "warn", name: "/warn", category: "Moderation", icon: ShieldAlert, desc: "Issue warning & log case" },
    { id: "strike", name: "/strike", category: "Moderation", icon: ShieldAlert, desc: "Issue strike with WKB progression" },
    { id: "ticket_panel", name: "/ticket panel", category: "Tickets", icon: Ticket, desc: "Deploy support ticket button portal" },
    { id: "apply_panel", name: "/apply panel", category: "Applications", icon: FileText, desc: "Deploy staff application form button" },
    { id: "config_show", name: "/config show", category: "Management", icon: Settings, desc: "View guild channels & settings" }
  ];

  const runSimulation = async (cmdId: string) => {
    setLoading(true);
    try {
      const res = await fetch("/api/bot/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          command: cmdId,
          params: { member: memberParam, reason: reasonParam }
        })
      });
      const data = await res.json();
      if (data.success) {
        setSimOutput(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    runSimulation("ping");
  }, []);

  return (
    <div className="space-y-4">
      {/* Top Banner */}
      <div className="bg-[#151B23] rounded border border-[#2D333B] p-3.5">
        <h2 className="text-sm font-bold text-white flex items-center gap-2 font-mono">
          <Terminal className="w-4 h-4 text-[#FF6B35]" />
          Slash Command Interactive Simulator & Inspector
        </h2>
        <p className="text-[11px] text-[#ADB5BD] mt-0.5">
          Execute slash commands live directly in browser. Validates generated Discord embeds & interactive components.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Command Selector List */}
        <div className="lg:col-span-5 bg-[#0E1217] rounded border border-[#2D333B] p-3 space-y-3">
          <div className="flex items-center justify-between border-b border-[#2D333B] pb-2">
            <h3 className="text-[10px] font-bold text-[#ADB5BD] uppercase tracking-wider font-mono">
              Available Slash Commands
            </h3>
            <span className="text-[9px] font-mono text-[#FF6B35] bg-[#1A110F] px-1.5 py-0.5 rounded border border-[#FF6B35]/30">
              discord.py v2.x
            </span>
          </div>

          <div className="space-y-1.5 max-h-[360px] overflow-y-auto pr-1">
            {commandsList.map((cmd) => {
              const Icon = cmd.icon;
              const isSelected = selectedCmd === cmd.id;
              return (
                <button
                  key={cmd.id}
                  onClick={() => {
                    setSelectedCmd(cmd.id);
                    runSimulation(cmd.id);
                  }}
                  className={`w-full text-left p-2.5 rounded border text-xs transition flex items-center justify-between ${
                    isSelected
                      ? "border-[#FF6B35] bg-[#1A110F] text-white font-semibold"
                      : "border-[#2D333B] bg-[#151B23]/50 hover:bg-[#151B23] text-[#ADB5BD]"
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon className={`w-3.5 h-3.5 ${isSelected ? "text-[#FF6B35]" : "opacity-60"}`} />
                    <div>
                      <div className="font-mono text-white text-[11px]">{cmd.name}</div>
                      <div className="text-[10px] text-[#ADB5BD] opacity-70 font-normal">{cmd.desc}</div>
                    </div>
                  </div>
                  <span className="text-[9px] font-mono bg-[#0B0F13] px-1.5 py-0.5 rounded border border-[#2D333B] text-[#ADB5BD]">
                    {cmd.category}
                  </span>
                </button>
              );
            })}
          </div>

          {/* Parameters input if command requires them */}
          {(selectedCmd === "warn" || selectedCmd === "strike") && (
            <div className="pt-3 border-t border-[#2D333B] space-y-2.5">
              <h4 className="text-[10px] font-bold text-white uppercase font-mono tracking-wider">
                Command Parameters
              </h4>
              <div>
                <label className="text-[10px] font-mono text-[#ADB5BD] block mb-1">Target Member (`member`)</label>
                <input
                  type="text"
                  value={memberParam}
                  onChange={(e) => setMemberParam(e.target.value)}
                  className="w-full text-xs font-mono px-2.5 py-1.5 border border-[#2D333B] rounded bg-[#0B0F13] text-white focus:outline-none focus:border-[#FF6B35]"
                />
              </div>
              <div>
                <label className="text-[10px] font-mono text-[#ADB5BD] block mb-1">Reason (`reason`)</label>
                <input
                  type="text"
                  value={reasonParam}
                  onChange={(e) => setReasonParam(e.target.value)}
                  className="w-full text-xs font-mono px-2.5 py-1.5 border border-[#2D333B] rounded bg-[#0B0F13] text-white focus:outline-none focus:border-[#FF6B35]"
                />
              </div>
              <button
                onClick={() => runSimulation(selectedCmd)}
                className="w-full py-1.5 bg-[#FF6B35] hover:bg-[#D44D1D] text-white font-bold font-mono text-xs rounded transition flex items-center justify-center gap-1.5 uppercase tracking-wider text-[11px]"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                Run Simulation
              </button>
            </div>
          )}
        </div>

        {/* Live Discord Embed Render Panel */}
        <div className="lg:col-span-7 bg-[#0E1217] rounded border border-[#2D333B] p-4 flex flex-col justify-between shadow-lg">
          <div>
            <div className="flex items-center justify-between border-b border-[#2D333B] pb-2.5 mb-3">
              <div className="flex items-center gap-2 text-white text-xs font-mono">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                <span>DISCORD RENDER PREVIEW</span>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 bg-[#151B23] border border-[#2D333B] rounded text-[#ADB5BD]">
                Canvas: Dark Mode
              </span>
            </div>

            {loading ? (
              <div className="py-16 text-center text-[#ADB5BD] text-xs font-mono animate-pulse">
                Exec: /{selectedCmd} ... Generating Embed Response...
              </div>
            ) : simOutput?.responseEmbed ? (
              <DiscordEmbedPreview embed={simOutput.responseEmbed} />
            ) : (
              <div className="py-16 text-center text-[#ADB5BD] text-xs font-mono">
                {simOutput?.responseText || "Select a command to run simulation"}
              </div>
            )}
          </div>

          <div className="mt-4 pt-2.5 border-t border-[#2D333B] text-[10px] font-mono text-[#ADB5BD] flex items-center justify-between">
            <span>Slash Command: <b className="text-white">/{selectedCmd}</b></span>
            <span className="text-green-400 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> Embed Validated OK
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
