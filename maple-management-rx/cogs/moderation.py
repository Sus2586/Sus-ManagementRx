import discord
from discord.ext import commands
from discord import app_commands
import datetime
from database.database import db
from utils.embeds import EmbedBuilder
from utils.permissions import is_mod, can_moderate
from utils.helpers import parse_duration

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Issue an official warning to a member.")
    @app_commands.describe(member="Member to warn", reason="Reason for warning")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions to issue warnings.", ephemeral=True)
        if not can_moderate(interaction.user, member):
            return await interaction.response.send_message("❌ You cannot warn a member with equal or higher permissions.", ephemeral=True)

        warn_id = await db.add_warning(interaction.guild_id, member.id, interaction.user.id, reason)
        await db.log_mod_action(interaction.guild_id, member.id, str(member), interaction.user.id, str(interaction.user), "WARN", reason)

        embed = EmbedBuilder.success("Warning Issued", f"Issued Warning **#{warn_id}** to {member.mention}.\n**Reason:** {reason}")
        await interaction.response.send_message(embed=embed)

        # Notify warned user in DM
        try:
            dm_embed = EmbedBuilder.warning(
                f"Warning Received in {interaction.guild.name}",
                f"You received a warning from staff.\n**Reason:** {reason}"
            )
            await member.send(embed=dm_embed)
        except discord.HTTPException:
            pass

    @app_commands.command(name="warnings", description="View warning records for a user.")
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions to view warning history.", ephemeral=True)

        records = await db.get_warnings(interaction.guild_id, member.id)
        if not records:
            embed = EmbedBuilder.default(f"Warning History — {member}", "This user has clean record (0 warnings).")
            return await interaction.response.send_message(embed=embed)

        embed = EmbedBuilder.default(f"Warning History — {member}", f"Total Warnings: `{len(records)}`")
        for rec in records[:10]:
            embed.add_field(
                name=f"Warning #{rec['id']} — {rec['timestamp']}",
                value=f"**Reason:** {rec['reason']}\n**Mod ID:** `{rec['moderator_id']}`",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clearwarnings", description="Clear warning records for a user.")
    async def clearwarnings(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions to clear warnings.", ephemeral=True)

        count = await db.clear_warnings(interaction.guild_id, member.id)
        embed = EmbedBuilder.success("Warnings Cleared", f"Cleared `{count}` warning records for {member.mention}.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="timeout", description="Timeout/mute a member for a duration (e.g. 10m, 2h, 1d).")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "No reason provided"):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions.", ephemeral=True)
        if not can_moderate(interaction.user, member):
            return await interaction.response.send_message("❌ Cannot mute member with equal or higher permissions.", ephemeral=True)

        seconds = parse_duration(duration)
        if seconds <= 0:
            return await interaction.response.send_message("❌ Invalid duration format. Use e.g. `10m`, `2h`, `1d`.", ephemeral=True)

        until = discord.utils.utcnow() + datetime.timedelta(seconds=seconds)
        await member.timeout(until, reason=reason)
        await db.log_mod_action(interaction.guild_id, member.id, str(member), interaction.user.id, str(interaction.user), "TIMEOUT", f"{duration} — {reason}")

        embed = EmbedBuilder.success("Member Timed Out", f"Timed out {member.mention} for `{duration}`.\n**Reason:** {reason}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kick", description="Kick a member from the server.")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions.", ephemeral=True)
        if not can_moderate(interaction.user, member):
            return await interaction.response.send_message("❌ Cannot kick member with equal or higher permissions.", ephemeral=True)

        await member.kick(reason=reason)
        await db.log_mod_action(interaction.guild_id, member.id, str(member), interaction.user.id, str(interaction.user), "KICK", reason)

        embed = EmbedBuilder.success("Member Kicked", f"Kicked {member.mention} from server.\n**Reason:** {reason}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ban", description="Ban a member from the server.")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions.", ephemeral=True)
        if not can_moderate(interaction.user, member):
            return await interaction.response.send_message("❌ Cannot ban member with equal or higher permissions.", ephemeral=True)

        await member.ban(reason=reason)
        await db.log_mod_action(interaction.guild_id, member.id, str(member), interaction.user.id, str(interaction.user), "BAN", reason)

        embed = EmbedBuilder.success("Member Banned", f"Banned {member.mention} from server.\n**Reason:** {reason}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unban", description="Unban a user by Discord User ID.")
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions.", ephemeral=True)
        try:
            uid = int(user_id)
            user = await self.bot.fetch_user(uid)
            await interaction.guild.unban(user, reason=reason)
            await db.log_mod_action(interaction.guild_id, uid, str(user), interaction.user.id, str(interaction.user), "UNBAN", reason)

            embed = EmbedBuilder.success("User Unbanned", f"Unbanned user `{user}` (`{uid}`).")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to unban user: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
