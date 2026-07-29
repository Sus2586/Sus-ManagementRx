# 🍁 Maple ManagementRx v2.0.0

**Phone-Only AI Development, Deployment & Management System**

Maple ManagementRx is a modular, production-ready Discord management & moderation bot engineered for zero-PC setup. The entire project can be generated, configured, deployed, tested, and maintained directly from an Android phone browser.

---

## 📱 Quick Android Phone Setup Checklist

Follow these step-by-step instructions directly from your Android mobile browser (Chrome / Edge / Firefox):

### Step 1: Create Your Bot on Discord Developer Portal
1. Open your browser on Android and navigate to: **[https://discord.com/developers/applications](https://discord.com/developers/applications)**.
2. If prompted, toggle **"Desktop Site"** in your browser options for optimal navigation.
3. Tap **New Application** in the top right.
4. Name the application **`Maple ManagementRx`** and agree to terms.
5. Tap **Bot** in the left sidebar menu.
6. Tap **Reset Token** or **Copy** to obtain your Bot Token. Save this token securely (e.g., in Bitwarden or a secure note).
7. Scroll down to **Privileged Gateway Intents**:
   - Enable **Server Members Intent** *(Required for staff tracking and member event logs)*.
   - Enable **Message Content Intent** *(Required for audit logging and moderation commands)*.
8. Tap **Save Changes**.

### Step 2: Generate Bot Invite URL
1. In Developer Portal, tap **OAuth2** -> **URL Generator**.
2. Under **Scopes**, check `bot` and `applications.commands`.
3. Under **Bot Permissions**, select:
   - `Manage Roles`
   - `Manage Channels`
   - `Kick Members`
   - `Ban Members`
   - `Moderate Members` (Timeout)
   - `Send Messages`
   - `Embed Links`
   - `Attach Files`
   - `Read Message History`
   - `Manage Messages`
4. Copy the generated URL at the bottom and paste it into your browser to invite the bot to your test Discord server.

### Step 3: Configure Environment Variables
Set the following environment variables in your deployment dashboard (or `.env` file):

```env
BOT_TOKEN=your_copied_discord_bot_token
BOT_NAME=Maple ManagementRx
BOT_VERSION=2.0.0
DEVELOPER=YourName
EMBED_COLOR=0xD97706
LOG_LEVEL=INFO
```

---

## 🚀 One-Tap Phone Cloud Deployment Options

You can host Maple ManagementRx 24/7 on free/affordable cloud providers right from your phone browser:

### Option A: Railway.app (Recommended for Mobile)
1. Open **[railway.app](https://railway.app)** on your phone.
2. Sign in with GitHub.
3. Tap **New Project** -> **Deploy from GitHub repo** -> Select `maple-management-rx`.
4. Tap **Variables** and add `BOT_TOKEN`.
5. Railway will automatically detect `requirements.txt` and launch `python bot.py`.

### Option B: Koyeb / Render
1. Sign into **koyeb.com** or **render.com**.
2. Select **Web Service / Worker**.
3. Connect your GitHub repository.
4. Set Build Command: `pip install -r requirements.txt`.
5. Set Run Command: `python bot.py`.
6. Add `BOT_TOKEN` under Environment Variables.

---

## 🏗️ Project Architecture

```
maple-management-rx/
├── bot.py                # Main Bot Entrypoint & Setup Hook
├── config.py             # Configuration & Environment Variables
├── requirements.txt      # Python Dependencies (discord.py, aiosqlite, python-dotenv)
├── README.md             # Android Phone User Guide
├── .env.example          # Environment Template
├── .gitignore            # Security rules (prevents token leaks)
│
├── cogs/                 # Modular Feature Cogs
│   ├── utility.py        # /ping, /about, /help commands
│   ├── moderation.py     # /warn, /kick, /ban, /timeout, /warnings
│   ├── management.py     # /strike, /strikes, /config commands
│   ├── tickets.py        # Support ticket panel & management
│   ├── applications.py   # Staff application workflow
│   ├── logging.py        # Audit log listeners (edits, deletes, joins)
│   └── admin.py          # Command sync & health checks
│
├── database/             # Async Persistence Layer
│   ├── database.py       # aiosqlite connection pool & queries
│   └── models.py         # Dataclasses and typing models
│
├── utils/                # Utility Helpers
│   ├── embeds.py         # Standardized Discord embed builder
│   ├── permissions.py    # Role & permission validation
│   └── helpers.py        # Time parsing & uptime formatting
│
└── views/                # Discord Interactive UI
    ├── buttons.py        # Ticket & application persistent buttons
    ├── modals.py         # Application forms & ticket rename modals
    └── selects.py        # Interactive dropdown help select menu
```

---

## 🛡️ Security & Zero-Leak Safeguards
- **No Hardcoded Tokens:** Secrets are loaded strictly from environment variables.
- **Git Protection:** `.gitignore` excludes `.env` and database files.
- **Permission Hierarchy:** Prevention against lower-ranked staff moderating higher-ranked staff or server owners.
