import discord
from discord.ext import commands
from discord import app_commands
from database.database import db
from utils.embeds import EmbedBuilder
from utils.permissions import is_mod, is_admin, can_moderate

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="strike", description="Issue a strike to a member with configurable escalation.")
    async def strike(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions.", ephemeral=True)
        if not can_moderate(interaction.user, member):
            return await interaction.response.send_message("❌ Cannot issue strike to member with equal or higher permissions.", ephemeral=True)

        settings = await db.get_guild_settings(interaction.guild_id)
        existing = await db.get_strikes(interaction.guild_id, member.id)
        strike_num = len(existing) + 1

        # Determine automated action based on strike progression
        if strike_num == 1:
            action_desc = settings.get("strike_1_action") or "Warning / Reminder"
        elif strike_num == 2:
            action_desc = settings.get("strike_2_action") or "Temporary Timeout (24h)"
            try:
                import datetime
                until = discord.utils.utcnow() + datetime.timedelta(hours=24)
                await member.timeout(until, reason=f"Strike #2 Escalation: {reason}")
            except Exception:
                pass
        else:
            action_desc = settings.get("strike_3_action") or "Kick / Ban Escalation"

        await db.add_strike(interaction.guild_id, member.id, interaction.user.id, reason, action_desc)
        await db.log_mod_action(interaction.guild_id, member.id, str(member), interaction.user.id, str(interaction.user), f"STRIKE_{strike_num}", reason)

        embed = EmbedBuilder.warning(
            f"Strike #{strike_num} Issued — {member}",
            f"**Member:** {member.mention}\n**Reason:** {reason}\n**Automatic Action:** {action_desc}"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="strikes", description="View active strike records for a user.")
    async def strikes(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ You require Moderator permissions.", ephemeral=True)

        records = await db.get_strikes(interaction.guild_id, member.id)
        if not records:
            embed = EmbedBuilder.default(f"Strike Records — {member}", "No active strikes found (0 strikes).")
            return await interaction.response.send_message(embed=embed)

        embed = EmbedBuilder.default(f"Strike Records — {member}", f"Active Strikes: `{len(records)}`")
        for rec in records:
            embed.add_field(
                name=f"Strike #{rec['strike_number']} — {rec['timestamp']}",
                value=f"**Reason:** {rec['reason']}\n**Action Taken:** {rec['action_taken']}\n**Mod ID:** `{rec['moderator_id']}`",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clearstrikes", description="Clear all strike records for a member.")
    async def clearstrikes(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_admin(interaction):
            return await interaction.response.send_message("❌ You require Administrator permissions to clear strikes.", ephemeral=True)

        count = await db.clear_strikes(interaction.guild_id, member.id)
        embed = EmbedBuilder.success("Strikes Cleared", f"Cleared `{count}` strike records for {member.mention}.")
        await interaction.response.send_message(embed=embed)

    # --- Guild Configuration Subcommands ---
    config_group = app_commands.Group(name="config", description="Configure Maple ManagementRx server settings.")

    @config_group.command(name="show", description="Display current guild configuration.")
    async def config_show(self, interaction: discord.Interaction):
        if not await is_admin(interaction):
            return await interaction.response.send_message("❌ Admin permissions required.", ephemeral=True)

        s = await db.get_guild_settings(interaction.guild_id)
        embed = EmbedBuilder.default("Maple Server Configuration", f"Current settings for `{interaction.guild.name}`:")
        embed.add_field(name="Log Channel", value=f"<#{s['log_channel_id']}>" if s['log_channel_id'] else "Not Configured", inline=True)
        embed.add_field(name="Mod Channel", value=f"<#{s['mod_channel_id']}>" if s['mod_channel_id'] else "Not Configured", inline=True)
        embed.add_field(name="Staff Channel", value=f"<#{s['staff_channel_id']}>" if s['staff_channel_id'] else "Not Configured", inline=True)
        embed.add_field(name="Staff Role", value=f"<@&{s['staff_role_id']}>" if s['staff_role_id'] else "Not Configured", inline=True)
        embed.add_field(name="Mod Role", value=f"<@&{s['mod_role_id']}>" if s['mod_role_id'] else "Not Configured", inline=True)
        embed.add_field(name="Admin Role", value=f"<@&{s['admin_role_id']}>" if s['admin_role_id'] else "Not Configured", inline=True)
        embed.add_field(name="Embed Color", value=f"`{s['embed_color']}`", inline=True)
        embed.add_field(name="WKB Escalation", value="Enabled" if s['wkb_enabled'] else "Disabled", inline=True)

        await interaction.response.send_message(embed=embed)

    @config_group.command(name="channels", description="Configure server channels.")
    async def config_channels(
        self, interaction: discord.Interaction,
        log_channel: discord.TextChannel = None,
        mod_channel: discord.TextChannel = None,
        staff_channel: discord.TextChannel = None
    ):
        if not await is_admin(interaction):
            return await interaction.response.send_message("❌ Admin permissions required.", ephemeral=True)

        if log_channel:
            await db.update_guild_setting(interaction.guild_id, "log_channel_id", log_channel.id)
        if mod_channel:
            await db.update_guild_setting(interaction.guild_id, "mod_channel_id", mod_channel.id)
        if staff_channel:
            await db.update_guild_setting(interaction.guild_id, "staff_channel_id", staff_channel.id)

        embed = EmbedBuilder.success("Configuration Updated", "Server channels have been saved.")
        await interaction.response.send_message(embed=embed)

    @config_group.command(name="roles", description="Configure server roles.")
    async def config_roles(
        self, interaction: discord.Interaction,
        staff_role: discord.Role = None,
        mod_role: discord.Role = None,
        admin_role: discord.Role = None
    ):
        if not await is_admin(interaction):
            return await interaction.response.send_message("❌ Admin permissions required.", ephemeral=True)

        if staff_role:
            await db.update_guild_setting(interaction.guild_id, "staff_role_id", staff_role.id)
        if mod_role:
            await db.update_guild_setting(interaction.guild_id, "mod_role_id", mod_role.id)
        if admin_role:
            await db.update_guild_setting(interaction.guild_id, "admin_role_id", admin_role.id)

        embed = EmbedBuilder.success("Roles Updated", "Staff & Moderation role permissions saved.")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Management(bot))
