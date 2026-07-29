import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import EmbedBuilder
from utils.permissions import is_admin
from views.buttons import ApplicationLaunchView

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    apply_group = app_commands.Group(name="apply", description="Application system controls.")

    @apply_group.command(name="panel", description="Deploy application submission panel.")
    async def apply_panel(self, interaction: discord.Interaction):
        if not await is_admin(interaction):
            return await interaction.response.send_message("❌ Admin permissions required.", ephemeral=True)

        embed = EmbedBuilder.default(
            "Maple Staff & Community Applications",
            "Interested in joining our server staff team? Click the button below to complete the application form."
        )
        embed.set_footer(text="Maple ManagementRx 2.0.0 Application Engine")

        await interaction.channel.send(embed=embed, view=ApplicationLaunchView())
        await interaction.response.send_message("✅ Application panel deployed!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Applications(bot))
