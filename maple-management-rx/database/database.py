import aiosqlite
import os
import json
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger("MapleBot.Database")

class Database:
    def __init__(self, db_path: str = "database/maple_bot.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)

    async def init_db(self):
        """Initializes sqlite database schemas asynchronously."""
        async with aiosqlite.connect(self.db_path) as db:
            # Guild settings
            await db.execute("""
                CREATE TABLE IF NOT EXISTS guild_settings (
                    guild_id INTEGER PRIMARY KEY,
                    log_channel_id INTEGER,
                    mod_channel_id INTEGER,
                    staff_channel_id INTEGER,
                    ticket_category_id INTEGER,
                    application_category_id INTEGER,
                    staff_role_id INTEGER,
                    mod_role_id INTEGER,
                    admin_role_id INTEGER,
                    embed_color TEXT DEFAULT '0xD97706',
                    wkb_enabled INTEGER DEFAULT 1,
                    strike_1_action TEXT DEFAULT 'Warning / Reminder',
                    strike_2_action TEXT DEFAULT 'Temporary Mute / Timeout (24h)',
                    strike_3_action TEXT DEFAULT 'Kick / Ban Escalation'
                )
            """)

            # Moderation logs & records
            await db.execute("""
                CREATE TABLE IF NOT EXISTS moderation_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    target_id INTEGER NOT NULL,
                    target_name TEXT,
                    moderator_id INTEGER NOT NULL,
                    moderator_name TEXT,
                    action_type TEXT NOT NULL,
                    reason TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Warnings
            await db.execute("""
                CREATE TABLE IF NOT EXISTS warnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    target_id INTEGER NOT NULL,
                    moderator_id INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Strikes
            await db.execute("""
                CREATE TABLE IF NOT EXISTS strikes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    target_id INTEGER NOT NULL,
                    strike_number INTEGER NOT NULL,
                    moderator_id INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    action_taken TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tickets
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    ticket_channel_id INTEGER UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    status TEXT DEFAULT 'open',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    closed_at TIMESTAMP,
                    closed_by INTEGER
                )
            """)

            # Applications
            await db.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    applicant_id INTEGER NOT NULL,
                    applicant_name TEXT,
                    application_name TEXT NOT NULL,
                    answers_json TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    reviewer_id INTEGER,
                    reviewer_comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Staff records
            await db.execute("""
                CREATE TABLE IF NOT EXISTS staff_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    staff_id INTEGER NOT NULL,
                    staff_name TEXT,
                    actions_count INTEGER DEFAULT 0,
                    warnings_issued INTEGER DEFAULT 0,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(guild_id, staff_id)
                )
            """)

            await db.commit()
            logger.info("Database schemas initialized successfully.")

    # --- Guild Settings Methods ---
    async def get_guild_settings(self, guild_id: int) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
                # Insert default settings
                await db.execute("INSERT OR IGNORE INTO guild_settings (guild_id) VALUES (?)", (guild_id,))
                await db.commit()
                return {
                    "guild_id": guild_id,
                    "log_channel_id": None,
                    "mod_channel_id": None,
                    "staff_channel_id": None,
                    "ticket_category_id": None,
                    "application_category_id": None,
                    "staff_role_id": None,
                    "mod_role_id": None,
                    "admin_role_id": None,
                    "embed_color": "0xD97706",
                    "wkb_enabled": 1,
                    "strike_1_action": "Warning / Reminder",
                    "strike_2_action": "Temporary Mute / Timeout (24h)",
                    "strike_3_action": "Kick / Ban Escalation"
                }

    async def update_guild_setting(self, guild_id: int, key: str, value: Any):
        await self.get_guild_settings(guild_id)  # Ensure row exists
        async with aiosqlite.connect(self.db_path) as db:
            query = f"UPDATE guild_settings SET {key} = ? WHERE guild_id = ?"
            await db.execute(query, (value, guild_id))
            await db.commit()

    # --- Moderation & Warnings ---
    async def add_warning(self, guild_id: int, target_id: int, moderator_id: int, reason: str) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO warnings (guild_id, target_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
                (guild_id, target_id, moderator_id, reason)
            )
            await db.commit()
            return cursor.lastrowid

    async def get_warnings(self, guild_id: int, target_id: int) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM warnings WHERE guild_id = ? AND target_id = ? ORDER BY timestamp DESC",
                (guild_id, target_id)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def clear_warnings(self, guild_id: int, target_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM warnings WHERE guild_id = ? AND target_id = ?", (guild_id, target_id))
            await db.commit()
            return cursor.rowcount

    # --- Strikes ---
    async def add_strike(self, guild_id: int, target_id: int, moderator_id: int, reason: str, action_taken: str) -> int:
        # Count existing strikes to determine strike number
        existing = await self.get_strikes(guild_id, target_id)
        strike_num = len(existing) + 1

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO strikes (guild_id, target_id, strike_number, moderator_id, reason, action_taken) VALUES (?, ?, ?, ?, ?, ?)",
                (guild_id, target_id, strike_num, moderator_id, reason, action_taken)
            )
            await db.commit()
            return strike_num

    async def get_strikes(self, guild_id: int, target_id: int) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM strikes WHERE guild_id = ? AND target_id = ? ORDER BY strike_number ASC",
                (guild_id, target_id)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def clear_strikes(self, guild_id: int, target_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM strikes WHERE guild_id = ? AND target_id = ?", (guild_id, target_id))
            await db.commit()
            return cursor.rowcount

    # --- Moderation Logs ---
    async def log_mod_action(self, guild_id: int, target_id: int, target_name: str, moderator_id: int, moderator_name: str, action_type: str, reason: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO moderation_actions (guild_id, target_id, target_name, moderator_id, moderator_name, action_type, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (guild_id, target_id, target_name, moderator_id, moderator_name, action_type, reason)
            )
            # Update staff record
            await db.execute("""
                INSERT INTO staff_records (guild_id, staff_id, staff_name, actions_count)
                VALUES (?, ?, ?, 1)
                ON CONFLICT(guild_id, staff_id) DO UPDATE SET
                    actions_count = actions_count + 1,
                    staff_name = excluded.staff_name,
                    last_active = CURRENT_TIMESTAMP
            """, (guild_id, moderator_id, moderator_name))
            await db.commit()

    # --- Tickets ---
    async def create_ticket(self, guild_id: int, channel_id: int, user_id: int, category: str) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO tickets (guild_id, ticket_channel_id, user_id, category) VALUES (?, ?, ?, ?)",
                (guild_id, channel_id, user_id, category)
            )
            await db.commit()
            return cursor.lastrowid

    async def close_ticket(self, channel_id: int, closed_by: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "UPDATE tickets SET status = 'closed', closed_at = CURRENT_TIMESTAMP, closed_by = ? WHERE ticket_channel_id = ?",
                (closed_by, channel_id)
            )
            await db.commit()
            return cursor.rowcount > 0

    # --- Applications ---
    async def create_application(self, guild_id: int, applicant_id: int, applicant_name: str, app_name: str, answers: dict) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO applications (guild_id, applicant_id, applicant_name, application_name, answers_json) VALUES (?, ?, ?, ?, ?)",
                (guild_id, applicant_id, applicant_name, app_name, json.dumps(answers))
            )
            await db.commit()
            return cursor.lastrowid

    async def update_application_status(self, app_id: int, status: str, reviewer_id: int, comment: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "UPDATE applications SET status = ?, reviewer_id = ?, reviewer_comment = ? WHERE id = ?",
                (status, reviewer_id, comment, app_id)
            )
            await db.commit()
            return cursor.rowcount > 0

db = Database()
