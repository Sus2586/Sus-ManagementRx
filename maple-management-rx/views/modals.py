import discord
import json
from database.database import db
from utils.embeds import EmbedBuilder

class TicketRenameModal(discord.ui.Modal, title="Rename Ticket Channel"):
    channel_name = discord.ui.TextInput(
        label="New Channel Name",
        placeholder="ticket-user-inquiry",
        required=True,
        max_length=32
    )

    async def on_submit(self, interaction: discord.Interaction):
        new_name = self.channel_name.value.strip().lower().replace(" ", "-")
        await interaction.channel.edit(name=new_name)
        embed = EmbedBuilder.success("Ticket Renamed", f"Channel renamed to `{new_name}`.")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ApplicationModal(discord.ui.Modal):
    def __init__(self, app_title: str, questions: list):
        super().__init__(title=f"Application: {app_title[:20]}")
        self.app_title = app_title
        self.inputs = []
        for q in questions[:5]:  # Discord modal max 5 inputs
            text_input = discord.ui.TextInput(
                label=q["label"],
                placeholder=q.get("placeholder", ""),
                style=discord.TextStyle.paragraph if q.get("long", False) else discord.TextStyle.short,
                required=q.get("required", True)
            )
            self.inputs.append(text_input)
            self.add_item(text_input)

    async def on_submit(self, interaction: discord.Interaction):
        answers = {inp.label: inp.value for inp in self.inputs}
        app_id = await db.create_application(
            guild_id=interaction.guild_id,
            applicant_id=interaction.user.id,
            applicant_name=str(interaction.user),
            app_name=self.app_title,
            answers=answers
        )

        embed = EmbedBuilder.success(
            "Application Submitted",
            f"Your application **#{app_id}** for **{self.app_title}** has been recorded and submitted to staff."
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Notify review channel if configured
        settings = await db.get_guild_settings(interaction.guild_id)
        mod_channel_id = settings.get("mod_channel_id") or settings.get("staff_channel_id")
        if mod_channel_id:
            channel = interaction.guild.get_channel(mod_channel_id)
            if channel:
                review_embed = EmbedBuilder.default(
                    f"New Application Received — #{app_id}",
                    f"**Applicant:** {interaction.user.mention} (`{interaction.user.id}`)\n**Type:** {self.app_title}"
                )
                for q, a in answers.items():
                    review_embed.add_field(name=q, value=a[:1000] or "N/A", inline=False)
                
                from views.buttons import ApplicationReviewView
                await channel.send(embed=review_embed, view=ApplicationReviewView(app_id=app_id))
