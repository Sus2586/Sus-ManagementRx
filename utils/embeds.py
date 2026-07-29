import discord
from datetime import datetime
import config

class EmbedBuilder:
    @staticmethod
    def default(title: str, description: str = "", color: int = None) -> discord.Embed:
        embed = discord.Embed(
            title=f"🍁 {title}",
            description=description,
            color=color or config.EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"{config.BOT_NAME} v{config.BOT_VERSION} | Moderation & Management", icon_url=None)
        return embed

    @staticmethod
    def success(title: str, description: str = "") -> discord.Embed:
        embed = discord.Embed(
            title=f"✅ {title}",
            description=description,
            color=0x10B981,  # Emerald Green
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"{config.BOT_NAME} v{config.BOT_VERSION}")
        return embed

    @staticmethod
    def warning(title: str, description: str = "") -> discord.Embed:
        embed = discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=0xF59E0B,  # Amber
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"{config.BOT_NAME} v{config.BOT_VERSION}")
        return embed

    @staticmethod
    def error(title: str, description: str = "") -> discord.Embed:
        embed = discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=0xEF4444,  # Red
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"{config.BOT_NAME} v{config.BOT_VERSION}")
        return embed

    @staticmethod
    def mod_log(action: str, target: discord.Member, moderator: discord.Member, reason: str, case_id: str = None) -> discord.Embed:
        embed = discord.Embed(
            title=f"🛡️ Moderation Log — {action.upper()}",
            color=0xDC2626 if action.lower() in ["ban", "kick"] else 0xF59E0B,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Target Member", value=f"{target.mention} (`{target.id}`)", inline=True)
        embed.add_field(name="Moderator", value=f"{moderator.mention} (`{moderator.id}`)", inline=True)
        if case_id:
            embed.add_field(name="Case ID", value=f"`#{case_id}`", inline=True)
        embed.add_field(name="Reason", value=reason or "No reason specified.", inline=False)
        embed.set_thumbnail(url=target.display_avatar.url if hasattr(target, "display_avatar") else "")
        embed.set_footer(text=f"{config.BOT_NAME} v{config.BOT_VERSION} Audit Log")
        return embed
