import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import EmbedBuilder
from utils.permissions import is_admin
import config

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    admin_group = app_commands.Group(name="admin", description="Bot administration and maintenance controls.")

    @admin_group.command(name="sync", description="Force sync slash commands across all guilds.")
    async def admin_sync(self, interaction: discord.Interaction):
        if not await is_admin(interaction):
            return await interaction.response.send_message("❌ Admin permissions required.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        synced = await self.bot.tree.sync()
        embed = EmbedBuilder.success("Slash Commands Synced", f"Successfully synced `{len(synced)}` application slash commands globally.")
        await interaction.followup.send(embed=embed)

    @admin_group.command(name="status", description="Inspect Maple ManagementRx internal system health.")
    async def admin_status(self, interaction: discord.Interaction):
        if not await is_admin(interaction):
            return await interaction.response.send_message("❌ Admin permissions required.", ephemeral=True)

        cogs_loaded = list(self.bot.cogs.keys())
        embed = EmbedBuilder.default("System Health & Cogs Overview", f"Active Bot Instance: **{config.BOT_NAME} v{config.BOT_VERSION}**")
        embed.add_field(name="Loaded Cogs", value=", ".join([f"`{c}`" for c in cogs_loaded]), inline=False)
        embed.add_field(name="Database Path", value=f"`{config.DATABASE_PATH}`", inline=False)
        embed.add_field(name="Log Level", value=f"`{config.LOG_LEVEL}`", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))
