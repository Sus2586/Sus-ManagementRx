import discord
from discord.ext import commands
from discord import app_commands
import time
from utils.embeds import EmbedBuilder
from utils.helpers import format_uptime
from views.selects import HelpView
import config

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Show bot latency, API response time, and status.")
    async def ping(self, interaction: discord.Interaction):
        start_time = time.perf_counter()
        await interaction.response.defer(ephemeral=False)
        end_time = time.perf_counter()

        api_latency = round((end_time - start_time) * 1000)
        ws_latency = round(self.bot.latency * 1000)

        embed = EmbedBuilder.default(
            title="Maple ManagementRx — Ping Status",
            description="Bot connection speeds and response latencies."
        )
        embed.add_field(name="🌐 WebSocket Latency", value=f"`{ws_latency} ms`", inline=True)
        embed.add_field(name="⚡ API Roundtrip", value=f"`{api_latency} ms`", inline=True)
        embed.add_field(name="🟢 System Status", value="`Operational`", inline=True)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="about", description="Display bot specs, developer info, server count & uptime.")
    async def about(self, interaction: discord.Interaction):
        uptime_str = format_uptime(self.bot.start_time)
        server_count = len(self.bot.guilds)
        total_users = sum(g.member_count or 0 for g in self.bot.guilds)

        embed = EmbedBuilder.default(
            title=f"About {config.BOT_NAME}",
            description="Maple ManagementRx is a modular, zero-PC management & moderation bot engineered for phone-native administration."
        )
        embed.add_field(name="🏷️ Version", value=f"`{config.BOT_VERSION}`", inline=True)
        embed.add_field(name="🐍 discord.py", value=f"`{discord.__version__}`", inline=True)
        embed.add_field(name="👑 Developer", value=f"`{config.DEVELOPER}`", inline=True)
        embed.add_field(name="🏰 Guilds", value=f"`{server_count}` servers", inline=True)
        embed.add_field(name="👥 Total Users", value=f"`{total_users}` members", inline=True)
        embed.add_field(name="⏱️ System Uptime", value=f"`{uptime_str}`", inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Interactive category-based help documentation.")
    async def help_cmd(self, interaction: discord.Interaction):
        embed = EmbedBuilder.default(
            title="Maple ManagementRx — Command Center",
            description="Select a category from the dropdown menu below to view detailed command guides."
        )
        await interaction.response.send_message(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Utility(bot))
