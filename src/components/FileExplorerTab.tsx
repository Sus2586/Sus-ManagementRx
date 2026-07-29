import React, { useState, useEffect } from "react";
import { Folder, FileCode, Copy, Check, Save, Download, ChevronRight, ChevronDown, FileText } from "lucide-react";

interface FileItem {
  name: string;
  path: string;
  type: "file" | "directory";
  size?: number;
  children?: FileItem[];
}

export const FileExplorerTab: React.FC = () => {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [activeFilePath, setActiveFilePath] = useState<string>("bot.py");
  const [fileContent, setFileContent] = useState<string>("");
  const [editedContent, setEditedContent] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [saving, setSaving] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);
  const [saveSuccess, setSaveSuccess] = useState<boolean>(false);
  const [openDirs, setOpenDirs] = useState<Record<string, boolean>>({ cogs: true, database: true, utils: true, views: true });

  const fetchFiles = async () => {
    try {
      const res = await fetch("/api/bot/files");
      const data = await res.json();
      if (data.success) {
        setFiles(data.files);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadFileContent = async (path: string) => {
    setLoading(true);
    setActiveFilePath(path);
    try {
      const res = await fetch(`/api/bot/file-content?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      if (data.success) {
        setFileContent(data.content);
        setEditedContent(data.content);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await fetch("/api/bot/save-file", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path: activeFilePath, content: editedContent })
      });
      const data = await res.json();
      if (data.success) {
        setFileContent(editedContent);
        setSaveSuccess(true);
        setTimeout(() => setSaveSuccess(false), 2000);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(editedContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  useEffect(() => {
    fetchFiles();
    loadFileContent("bot.py");
  }, []);

  const toggleDir = (dirPath: string) => {
    setOpenDirs(prev => ({ ...prev, [dirPath]: !prev[dirPath] }));
  };

  const renderTree = (items: FileItem[]) => {
    return items.map((item) => {
      if (item.type === "directory") {
        const isOpen = !!openDirs[item.path];
        return (
          <div key={item.path} className="select-none font-mono">
            <button
              onClick={() => toggleDir(item.path)}
              className="w-full text-left py-1 px-2 hover:bg-[#151B23] rounded text-[11px] font-semibold text-white flex items-center gap-1.5"
            >
              {isOpen ? <ChevronDown className="w-3.5 h-3.5 opacity-60" /> : <ChevronRight className="w-3.5 h-3.5 opacity-60" />}
              <Folder className="w-3.5 h-3.5 text-[#FF6B35]" />
              <span>{item.name}/</span>
            </button>
            {isOpen && item.children && (
              <div className="pl-3 border-l border-[#2D333B] ml-2.5 my-0.5 space-y-0.5">
                {renderTree(item.children)}
              </div>
            )}
          </div>
        );
      }
      const isActive = activeFilePath === item.path;
      return (
        <button
          key={item.path}
          onClick={() => loadFileContent(item.path)}
          className={`w-full text-left py-1 px-2 rounded text-[11px] font-mono flex items-center justify-between transition ${
            isActive
              ? "bg-[#1A110F] text-[#FF6B35] font-semibold border-l-2 border-[#FF6B35]"
              : "hover:bg-[#151B23] text-[#ADB5BD]"
          }`}
        >
          <div className="flex items-center gap-1.5 truncate">
            <FileCode className={`w-3.5 h-3.5 ${isActive ? "text-[#FF6B35]" : "opacity-40"}`} />
            <span className="truncate">{item.name}</span>
          </div>
        </button>
      );
    });
  };

  return (
    <div className="space-y-4">
      <div className="bg-[#151B23] rounded border border-[#2D333B] p-3.5">
        <h2 className="text-sm font-bold text-white flex items-center gap-2 font-mono">
          <FileCode className="w-4 h-4 text-[#FF6B35]" />
          Python Project File Explorer & Code Editor
        </h2>
        <p className="text-[11px] text-[#ADB5BD] mt-0.5">
          Inspect, edit, copy, or maintain the complete modular Python bot codebase directly in browser.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Directory Sidebar */}
        <div className="lg:col-span-4 bg-[#0E1217] rounded border border-[#2D333B] p-3">
          <div className="flex items-center justify-between border-b border-[#2D333B] pb-2 mb-2 bg-[#151B23] px-2.5 py-1.5 rounded text-[10px] font-mono">
            <span className="font-bold text-white uppercase tracking-wider">
              Project Structure
            </span>
            <span className="text-[#FF6B35] font-semibold">
              15 FILES
            </span>
          </div>

          <div className="space-y-0.5 max-h-[500px] overflow-y-auto pr-1">
            {renderTree(files)}
          </div>
        </div>

        {/* Code Editor */}
        <div className="lg:col-span-8 bg-[#0E1217] rounded border border-[#2D333B] p-3.5 shadow-lg flex flex-col justify-between">
          <div>
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#2D333B] pb-2.5 mb-3 bg-[#151B23] p-2 rounded">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-[#FF6B35]" />
                <span className="text-xs font-mono font-bold text-white">{activeFilePath}</span>
                {editedContent !== fileContent && (
                  <span className="text-[9px] bg-[#FF6B35]/20 text-[#FF6B35] border border-[#FF6B35]/40 px-1.5 py-0.5 rounded font-mono uppercase">
                    MODIFIED
                  </span>
                )}
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopy}
                  className="px-2.5 py-1 bg-[#0B0F13] hover:bg-[#151B23] text-white text-[10px] font-mono font-bold rounded transition flex items-center gap-1 border border-[#2D333B]"
                >
                  {copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}
                  {copied ? "COPIED" : "COPY"}
                </button>
                <button
                  onClick={handleSave}
                  disabled={saving || editedContent === fileContent}
                  className={`px-3 py-1 text-[10px] font-mono font-bold rounded transition flex items-center gap-1 uppercase ${
                    editedContent !== fileContent
                      ? "bg-[#FF6B35] hover:bg-[#D44D1D] text-white"
                      : "bg-[#151B23] text-gray-500 cursor-not-allowed border border-[#2D333B]"
                  }`}
                >
                  <Save className="w-3 h-3" />
                  {saveSuccess ? "SAVED!" : saving ? "SAVING..." : "SAVE FILE"}
                </button>
              </div>
            </div>

            {loading ? (
              <div className="py-20 text-center text-[#ADB5BD] text-xs font-mono animate-pulse">
                Reading file system stream...
              </div>
            ) : (
              <textarea
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
                spellCheck={false}
                className="w-full h-[450px] bg-[#0B0F13] text-[#ADB5BD] font-mono text-xs p-3 rounded border border-[#2D333B] focus:outline-none focus:border-[#FF6B35] leading-relaxed resize-none selection:bg-[#FF6B35]/30"
              />
            )}
          </div>

          <div className="mt-3 pt-2 border-t border-[#2D333B] text-[10px] text-[#ADB5BD] flex items-center justify-between font-mono">
            <span>Encoding: UTF-8 • Runtime: Python 3.12+</span>
            <span>Total Lines: {editedContent.split("\n").length}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
