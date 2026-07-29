import React, { useState } from "react";
import { Smartphone, CheckCircle2, Circle, ExternalLink, ShieldAlert, Key, Server, GitBranch, Sparkles } from "lucide-react";

export const PhoneGuideTab: React.FC = () => {
  const [completedSteps, setCompletedSteps] = useState<Record<string, boolean>>({
    step1: true,
    step2: false,
    step3: false,
    step4: false,
    step5: false
  });

  const toggleStep = (key: string) => {
    setCompletedSteps((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const steps = [
    {
      id: "step1",
      title: "1. Create Discord Application on Phone Browser",
      icon: Smartphone,
      details: [
        "Open Chrome/Firefox on Android and navigate to discord.com/developers/applications.",
        "Tip: In your browser menu, check 'Desktop site' for standard navigation.",
        "Tap 'New Application' at top right and name it Maple ManagementRx.",
        "Agree to developer terms and create the application."
      ],
      link: { url: "https://discord.com/developers/applications", label: "Open Discord Developer Portal" }
    },
    {
      id: "step2",
      title: "2. Generate Bot Token & Enable Privileged Intents",
      icon: Key,
      details: [
        "In the left menu, select Bot.",
        "Tap 'Reset Token' or 'Copy' to retrieve your Bot Token securely.",
        "Scroll down to Privileged Gateway Intents:",
        "• Enable Server Members Intent (Needed for staff logging & joins)",
        "• Enable Message Content Intent (Needed for moderation & logging)",
        "Tap 'Save Changes'."
      ]
    },
    {
      id: "step3",
      title: "3. Invite Bot to Test Server",
      icon: ExternalLink,
      details: [
        "Go to OAuth2 -> URL Generator in Developer Portal.",
        "Under Scopes, check 'bot' and 'applications.commands'.",
        "Under Bot Permissions, select Administrator OR specific permissions: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members, Send Messages, Embed Links.",
        "Copy the generated URL at the bottom and open it in a browser tab to invite the bot to your Discord server."
      ]
    },
    {
      id: "step4",
      title: "4. Deploy to 24/7 Cloud Hosting (Railway / Koyeb)",
      icon: Server,
      details: [
        "Sign into Railway.app or Koyeb.com from your phone browser.",
        "Select 'New Service' -> 'Deploy from GitHub' -> Select maple-management-rx repo.",
        "In the Railway/Koyeb dashboard, tap Variables / Environment Secrets.",
        "Add key BOT_TOKEN with your copied bot token value.",
        "Deployment platform automatically installs requirements.txt and executes python bot.py 24/7!"
      ],
      link: { url: "https://railway.app", label: "Open Railway Hosting" }
    },
    {
      id: "step5",
      title: "5. GitHub Mobile App Integration",
      icon: GitBranch,
      details: [
        "Download GitHub Mobile app on Android from Google Play Store if desired.",
        "Sign in to push code edits or view automated build commits.",
        "Ensure .env and bot token are NEVER committed to public repositories."
      ]
    }
  ];

  const doneCount = Object.values(completedSteps).filter(Boolean).length;

  return (
    <div className="space-y-4">
      {/* Banner */}
      <div className="bg-[#151B23] rounded border border-[#2D333B] p-3.5">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-[#FF6B35] to-[#D44D1D] flex items-center justify-center text-white font-bold text-sm shadow-sm">
            📱
          </div>
          <div>
            <h2 className="text-sm font-bold text-white font-mono">
              Android Management Control Console (Zero-PC Mode)
            </h2>
            <p className="text-[11px] text-[#ADB5BD] opacity-70 mt-0.5">
              Step-by-step mobile browser setup & deployment checklist.
            </p>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-[#0E1217] p-3.5 rounded border border-[#2D333B] space-y-2">
        <div className="flex items-center justify-between text-xs font-mono font-bold text-white">
          <span>SETUP CHECKLIST PROGRESS</span>
          <span className="text-[#FF6B35]">
            {doneCount} / {steps.length} COMPLETED ({Math.round((doneCount / steps.length) * 100)}%)
          </span>
        </div>
        <div className="w-full h-2 bg-[#0B0F13] rounded-full overflow-hidden border border-[#2D333B]">
          <div
            className="h-full bg-[#FF6B35] transition-all duration-300"
            style={{
              width: `${(doneCount / steps.length) * 100}%`
            }}
          ></div>
        </div>
      </div>

      {/* Steps List */}
      <div className="space-y-3">
        {steps.map((step) => {
          const isDone = !!completedSteps[step.id];
          return (
            <div
              key={step.id}
              className={`bg-[#0E1217] rounded border p-4 transition ${
                isDone ? "border-green-500/40 bg-green-500/5" : "border-[#2D333B]"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-3">
                  <button
                    onClick={() => toggleStep(step.id)}
                    className="mt-0.5 text-gray-400 hover:text-green-400 transition focus:outline-none"
                  >
                    {isDone ? (
                      <CheckCircle2 className="w-5 h-5 text-green-400 fill-green-500/20" />
                    ) : (
                      <Circle className="w-5 h-5 text-gray-500" />
                    )}
                  </button>
                  <div>
                    <h3 className={`font-mono font-bold text-xs ${isDone ? "text-green-400 line-through" : "text-white"}`}>
                      {step.title}
                    </h3>
                    <ul className="mt-2 space-y-1 text-[11px] font-mono text-[#ADB5BD]">
                      {step.details.map((detail, idx) => (
                        <li key={idx} className="flex items-start gap-1.5">
                          <span className="text-[#FF6B35] font-bold">•</span>
                          <span>{detail}</span>
                        </li>
                      ))}
                    </ul>

                    {step.link && (
                      <a
                        href={step.link.url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-[10px] font-mono font-bold text-[#FF6B35] hover:underline mt-2.5 uppercase tracking-wider"
                      >
                        {step.link.label}
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
