import discord
from discord.ext import commands
from discord import app_commands
from database.database import db
from utils.embeds import EmbedBuilder
from utils.permissions import is_admin, is_staff
from views.buttons import TicketLaunchView

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ticket_group = app_commands.Group(name="ticket", description="Ticket system controls.")

    @ticket_group.command(name="panel", description="Deploy a persistent ticket launch panel in the current channel.")
    async def ticket_panel(self, interaction: discord.Interaction):
        if not await is_admin(interaction):
            return await interaction.response.send_message("❌ Administrator permissions required to deploy ticket panel.", ephemeral=True)

        embed = EmbedBuilder.default(
            "Maple Support Ticket Portal",
            "Need help or wish to contact staff? Click the button below to open a private ticket channel."
        )
        embed.add_field(name="Available Categories", value="• General Support\n• Staff Support\n• Management / Report\n• Other Inquiries", inline=False)
        embed.set_footer(text="Maple ManagementRx 2.0.0 Ticket Engine")

        await interaction.channel.send(embed=embed, view=TicketLaunchView())
        await interaction.response.send_message("✅ Persistent Ticket panel deployed successfully!", ephemeral=True)

    @ticket_group.command(name="add", description="Add a member to the current ticket channel.")
    async def ticket_add(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_staff(interaction):
            return await interaction.response.send_message("❌ Staff permission required.", ephemeral=True)

        await interaction.channel.set_permissions(member, read_messages=True, send_messages=True, attach_files=True)
        embed = EmbedBuilder.success("Member Added", f"Added {member.mention} to ticket.")
        await interaction.response.send_message(embed=embed)

    @ticket_group.command(name="remove", description="Remove a member from the current ticket channel.")
    async def ticket_remove(self, interaction: discord.Interaction, member: discord.Member):
        if not await is_staff(interaction):
            return await interaction.response.send_message("❌ Staff permission required.", ephemeral=True)

        await interaction.channel.set_permissions(member, overwrite=None)
        embed = EmbedBuilder.warning("Member Removed", f"Removed {member.mention} from ticket.")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
