import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_NAME = os.getenv("BOT_NAME", "Maple ManagementRx")
BOT_VERSION = os.getenv("BOT_VERSION", "2.0.0")
DEVELOPER = os.getenv("DEVELOPER", "Maple Development Team")
RAW_COLOR = os.getenv("EMBED_COLOR", "0xD97706")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATABASE_PATH = os.getenv("DATABASE_PATH", "database/maple_bot.db")

try:
    if RAW_COLOR.startswith("0x") or RAW_COLOR.startswith("0X"):
        EMBED_COLOR = int(RAW_COLOR, 16)
    elif RAW_COLOR.startswith("#"):
        EMBED_COLOR = int(RAW_COLOR[1:], 16)
    else:
        EMBED_COLOR = int(RAW_COLOR)
except ValueError:
    EMBED_COLOR = 0xD97706  # Maple Amber Gold default
