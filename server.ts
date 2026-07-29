import express from "express";
import path from "path";
import fs from "fs";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI } from "@google/genai";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = 3000;

app.use(express.json());

// Initialize Gemini AI lazily for server-side requests
let aiClient: GoogleGenAI | null = null;
function getAIClient(): GoogleGenAI {
  if (!aiClient) {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error("GEMINI_API_KEY environment variable is missing.");
    }
    aiClient = new GoogleGenAI({ apiKey });
  }
  return aiClient;
}

// ================= API ENDPOINTS =================

// 1. Get project files list
app.get("/api/bot/files", (req, res) => {
  const rootDir = path.join(process.cwd(), "maple-management-rx");
  
  function scanDir(dir: string, relativePath: string = ""): any[] {
    if (!fs.existsSync(dir)) return [];
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    let results: any[] = [];

    for (const entry of entries) {
      if (entry.name === "__pycache__" || entry.name.endsWith(".pyc")) continue;
      const fullPath = path.join(dir, entry.name);
      const relPath = relativePath ? `${relativePath}/${entry.name}` : entry.name;

      if (entry.isDirectory()) {
        results.push({
          name: entry.name,
          path: relPath,
          type: "directory",
          children: scanDir(fullPath, relPath)
        });
      } else {
        const stats = fs.statSync(fullPath);
        results.push({
          name: entry.name,
          path: relPath,
          type: "file",
          size: stats.size
        });
      }
    }
    return results;
  }

  const fileTree = scanDir(rootDir);
  res.json({ success: true, files: fileTree });
});

// 2. Read specific file content
app.get("/api/bot/file-content", (req, res) => {
  const filePath = req.query.path as string;
  if (!filePath) {
    return res.status(400).json({ error: "File path required" });
  }

  const fullPath = path.join(process.cwd(), "maple-management-rx", filePath);
  if (!fs.existsSync(fullPath)) {
    return res.status(404).json({ error: "File not found" });
  }

  try {
    const content = fs.readFileSync(fullPath, "utf-8");
    res.json({ success: true, path: filePath, content });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// 3. Save modified file content
app.post("/api/bot/save-file", (req, res) => {
  const { path: filePath, content } = req.body;
  if (!filePath || content === undefined) {
    return res.status(400).json({ error: "Path and content required" });
  }

  const fullPath = path.join(process.cwd(), "maple-management-rx", filePath);
  try {
    fs.mkdirSync(path.dirname(fullPath), { recursive: true });
    fs.writeFileSync(fullPath, content, "utf-8");
    res.json({ success: true, message: `File ${filePath} updated successfully.` });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// 4. Simulate Discord Slash Commands with rich Embed preview outputs
app.post("/api/bot/simulate", (req, res) => {
  const { command, params = {} } = req.body;
  const now = new Date().toISOString();

  let responseEmbed: any = null;
  let responseText = "";

  switch (command) {
    case "ping":
      responseEmbed = {
        title: "🍁 Maple ManagementRx — Ping Status",
        description: "Bot connection speeds and response latencies.",
        color: "#D97706",
        fields: [
          { name: "🌐 WebSocket Latency", value: "`34 ms`", inline: true },
          { name: "⚡ API Roundtrip", value: "`88 ms`", inline: true },
          { name: "🟢 System Status", value: "`Operational`", inline: true }
        ],
        footer: "Maple ManagementRx v2.0.0 | Moderation & Management",
        timestamp: now
      };
      break;

    case "about":
      responseEmbed = {
        title: "About Maple ManagementRx",
        description: "Maple ManagementRx is a modular, zero-PC management & moderation bot engineered for phone-native administration.",
        color: "#D97706",
        fields: [
          { name: "🏷️ Version", value: "`2.0.0`", inline: true },
          { name: "🐍 discord.py", value: "`2.3.2`", inline: true },
          { name: "👑 Developer", value: "`Maple Development Team`", inline: true },
          { name: "🏰 Guilds", value: "`14` servers", inline: true },
          { name: "👥 Total Users", value: "`18,450` members", inline: true },
          { name: "⏱️ System Uptime", value: "`4d 12h 30m`", inline: true }
        ],
        footer: "Maple ManagementRx v2.0.0",
        timestamp: now
      };
      break;

    case "help":
      responseEmbed = {
        title: "Maple ManagementRx — Command Center",
        description: "Interactive category dropdown active. Categories include Utility, Moderation & Strikes, Server Config, Ticket System, Applications, and Admin.",
        color: "#D97706",
        fields: [
          { name: "🛠️ Utility", value: "`/ping`, `/about`, `/help`", inline: false },
          { name: "🛡️ Moderation", value: "`/warn`, `/warnings`, `/clearwarnings`, `/timeout`, `/kick`, `/ban`, `/unban`", inline: false },
          { name: "⚙️ Management", value: "`/strike`, `/strikes`, `/clearstrikes`, `/config`", inline: false },
          { name: "🎫 Tickets", value: "`/ticket panel`, `/ticket add`, `/ticket remove`", inline: false },
          { name: "📋 Applications", value: "`/apply panel`", inline: false }
        ],
        footer: "Maple ManagementRx v2.0.0 | Command Guide",
        timestamp: now
      };
      break;

    case "warn":
      const warnUser = params.member || "@UserMember";
      const warnReason = params.reason || "Violating server rule #3";
      responseEmbed = {
        title: "✅ Warning Issued",
        description: `Issued Warning **#104** to **${warnUser}**.\n**Reason:** ${warnReason}`,
        color: "#10B981",
        footer: "Maple ManagementRx v2.0.0 | Audit Logged",
        timestamp: now
      };
      break;

    case "strike":
      const strikeUser = params.member || "@UserMember";
      const strikeReason = params.reason || "Repeated spam in general chat";
      responseEmbed = {
        title: "⚠️ Strike #2 Issued — " + strikeUser,
        description: `**Member:** ${strikeUser}\n**Reason:** ${strikeReason}\n**Automatic Action:** Temporary Mute / Timeout (24h)`,
        color: "#F59E0B",
        footer: "Maple ManagementRx v2.0.0 | WKB Escalation Engine",
        timestamp: now
      };
      break;

    case "ticket_panel":
      responseEmbed = {
        title: "Maple Support Ticket Portal",
        description: "Need help or wish to contact staff? Click the button below to open a private ticket channel.",
        color: "#D97706",
        fields: [
          { name: "Available Categories", value: "• General Support\n• Staff Support\n• Management / Report\n• Other Inquiries", inline: false }
        ],
        footer: "Maple ManagementRx 2.0.0 Ticket Engine",
        timestamp: now,
        interactiveButtons: [
          { label: "Open Support Ticket", style: "primary", emoji: "🎫" }
        ]
      };
      break;

    case "apply_panel":
      responseEmbed = {
        title: "Maple Staff & Community Applications",
        description: "Interested in joining our server staff team? Click the button below to complete the application form.",
        color: "#D97706",
        footer: "Maple ManagementRx 2.0.0 Application Engine",
        timestamp: now,
        interactiveButtons: [
          { label: "Apply Now", style: "primary", emoji: "📋" }
        ]
      };
      break;

    case "config_show":
      responseEmbed = {
        title: "Maple Server Configuration",
        description: "Current settings for `Maple Community Server`:",
        color: "#D97706",
        fields: [
          { name: "Log Channel", value: "<#log-events>", inline: true },
          { name: "Mod Channel", value: "<#mod-logs>", inline: true },
          { name: "Staff Channel", value: "<#staff-lounge>", inline: true },
          { name: "Staff Role", value: "<@&Staff>", inline: true },
          { name: "Mod Role", value: "<@&Moderator>", inline: true },
          { name: "Admin Role", value: "<@&Admin>", inline: true },
          { name: "Embed Color", value: "`0xD97706`", inline: true },
          { name: "WKB Escalation", value: "Enabled", inline: true }
        ],
        footer: "Maple ManagementRx Settings",
        timestamp: now
      };
      break;

    default:
      responseText = `Executed slash command: /${command}`;
      break;
  }

  res.json({
    success: true,
    command,
    responseEmbed,
    responseText
  });
});

// 5. AI Assistant endpoint for Phone Bot Customization
app.post("/api/ai/assistant", async (req, res) => {
  const { prompt } = req.body;
  if (!prompt) {
    return res.status(400).json({ error: "Prompt is required" });
  }

  try {
    const ai = getAIClient();
    const systemInstruction = `You are the Maple ManagementRx v2.0.0 AI Development Companion. 
    You assist developers configuring their Python discord.py bot directly from their Android phone browser.
    Provide concise, phone-optimized explanations, code snippets, or setup guidance.`;

    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: prompt,
      config: {
        systemInstruction
      }
    });

    res.json({ success: true, answer: response.text });
  } catch (err: any) {
    console.error("AI assistant error:", err);
    res.status(500).json({ error: err.message || "Failed to generate response." });
  }
});

// ================= VITE MIDDLEWARE SETUP =================

async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://0.0.0.0:${PORT}`);
  });
}

startServer();
