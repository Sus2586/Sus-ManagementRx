import React, { useState } from "react";
import { LayoutDashboard, Terminal, FolderGit2, Smartphone, Sparkles, Download, Github, Shield } from "lucide-react";
import { DashboardTab } from "./components/DashboardTab";
import { SimulatorTab } from "./components/SimulatorTab";
import { FileExplorerTab } from "./components/FileExplorerTab";
import { PhoneGuideTab } from "./components/PhoneGuideTab";
import { AIAssistantTab } from "./components/AIAssistantTab";

export default function App() {
  const [activeTab, setActiveTab] = useState<"dashboard" | "simulator" | "files" | "guide" | "ai">("dashboard");

  const navItems = [
    { id: "dashboard", label: "Control Deck", icon: LayoutDashboard },
    { id: "simulator", label: "Command Tester", icon: Terminal },
    { id: "files", label: "Python Files", icon: FolderGit2 },
    { id: "guide", label: "Android Setup", icon: Smartphone },
    { id: "ai", label: "AI Companion", icon: Sparkles }
  ];

  return (
    <div className="min-h-screen bg-[#0B0F13] text-[#ADB5BD] font-sans selection:bg-[#FF6B35]/20 selection:text-white flex flex-col">
      {/* High Density Header */}
      <header className="bg-[#151B23] border-b border-[#2D333B] sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-2.5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-gradient-to-br from-[#FF6B35] to-[#D44D1D] flex items-center justify-center text-white font-bold text-base shadow-sm">
              M
            </div>
            <div>
              <h1 className="font-bold text-sm text-white tracking-tight leading-none flex items-center gap-1.5">
                Maple ManagementRx <span className="text-[#FF6B35] text-[10px] font-mono">v2.0.0</span>
              </h1>
              <p className="text-[10px] text-[#ADB5BD] opacity-70 mt-0.5">
                Production-Ready Discord Management Engine • Zero-PC Architecture
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 bg-[#0B0F13] border border-[#2D333B] rounded text-[10px] font-mono">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              <span className="text-white font-semibold">CLOUD-RUNNING</span>
            </div>
            <a
              href="https://discord.com/developers/applications"
              target="_blank"
              rel="noreferrer"
              className="text-xs px-3 py-1.5 rounded bg-[#FF6B35] hover:bg-[#D44D1D] font-bold text-white transition flex items-center gap-1.5 uppercase tracking-wider text-[11px]"
            >
              <Shield className="w-3.5 h-3.5" />
              Dev Portal
            </a>
          </div>
        </div>

        {/* Dense Tab Navigation */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 overflow-x-auto">
          <nav className="flex space-x-1 border-t border-[#2D333B] pt-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id as any)}
                  className={`px-3.5 py-2 text-xs font-semibold rounded-t transition flex items-center gap-2 whitespace-nowrap ${
                    isActive
                      ? "bg-[#0E1217] text-white border-b-2 border-[#FF6B35]"
                      : "text-[#ADB5BD] hover:text-white hover:bg-[#151B23]/60"
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? "text-[#FF6B35]" : "opacity-60"}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-5 flex-1 w-full">
        {activeTab === "dashboard" && <DashboardTab />}
        {activeTab === "simulator" && <SimulatorTab />}
        {activeTab === "files" && <FileExplorerTab />}
        {activeTab === "guide" && <PhoneGuideTab />}
        {activeTab === "ai" && <AIAssistantTab />}
      </main>

      {/* High Density Footer */}
      <footer className="border-t border-[#2D333B] bg-[#0E1217] px-4 py-3 text-[10px] font-mono text-[#ADB5BD]">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center gap-3">
            <span>Connected Shards: <b className="text-white">4/4</b></span>
            <span>Gateway: <b className="text-white">v10.0</b></span>
            <span>Runtime: <b className="text-white">CPython 3.12.2</b></span>
          </div>
          <div className="flex items-center gap-4 text-slate-400">
            <span className="text-[#FF6B35] font-semibold">Maple Rx v2.0.0</span>
            <span>discord.py 2.4.0</span>
            <span>aiosqlite</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
