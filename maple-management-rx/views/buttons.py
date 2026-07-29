import discord
import io
import datetime
import config
from database.database import db
from utils.embeds import EmbedBuilder
from utils.permissions import is_staff, is_mod

async def create_ticket_channel(interaction: discord.Interaction, category: str):
    guild = interaction.guild
    settings = await db.get_guild_settings(guild.id)
    category_id = settings.get("ticket_category_id")

    ticket_category = guild.get_channel(category_id) if category_id else None

    # Channel permissions setup
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
    }

    # Add staff role overwrite if configured
    staff_role_id = settings.get("staff_role_id") or settings.get("mod_role_id")
    if staff_role_id:
        role = guild.get_role(staff_role_id)
        if role:
            overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    clean_user = interaction.user.name.lower().replace(" ", "-")
    channel_name = f"ticket-{clean_user}"

    ticket_channel = await guild.create_text_channel(
        name=channel_name,
        category=ticket_category,
        overwrites=overwrites,
        reason=f"Ticket opened by {interaction.user}"
    )

    ticket_id = await db.create_ticket(
        guild_id=guild.id,
        channel_id=ticket_channel.id,
        user_id=interaction.user.id,
        category=category
    )

    embed = EmbedBuilder.default(
        f"Ticket #{ticket_id} — {category}",
        f"Welcome {interaction.user.mention}! Staff has been notified. Describe your issue or request below."
    )
    embed.add_field(name="Category", value=category, inline=True)
    embed.add_field(name="Opened By", value=interaction.user.mention, inline=True)

    await ticket_channel.send(embed=embed, view=TicketControlView())
    await interaction.response.send_message(
        f"✅ Ticket created! Head over to {ticket_channel.mention}", ephemeral=True
    )


class TicketLaunchView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Support Ticket", style=discord.ButtonStyle.primary, emoji="🎫", custom_id="maple_open_ticket_btn")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.selects import TicketCategorySelect
        view = discord.ui.View()
        view.add_item(TicketCategorySelect())
        await interaction.response.send_message("Please select a category for your ticket:", view=view, ephemeral=True)


class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="maple_ticket_close_btn")
    async def close_ticket_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await db.close_ticket(interaction.channel_id, interaction.user.id)
        
        # Generate basic transcript text
        messages = []
        async for msg in interaction.channel.history(limit=500, oldest_first=True):
            messages.append(f"[{msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {msg.author}: {msg.content}")

        transcript_text = f"=== MAPLE MANAGEMENT RX TICKET TRANSCRIPT ===\nChannel: {interaction.channel.name}\nClosed By: {interaction.user}\nDate: {datetime.datetime.utcnow()}\n\n" + "\n".join(messages)

        transcript_file = discord.File(
            fp=io.BytesIO(transcript_text.encode("utf-8")),
            filename=f"transcript-{interaction.channel.name}.txt"
        )

        settings = await db.get_guild_settings(interaction.guild_id)
        log_channel_id = settings.get("log_channel_id")
        if log_channel_id:
            log_chan = interaction.guild.get_channel(log_channel_id)
            if log_chan:
                log_embed = EmbedBuilder.default(
                    "Ticket Closed",
                    f"**Channel:** {interaction.channel.name}\n**Closed By:** {interaction.user.mention}"
                )
                await log_chan.send(embed=log_embed, file=transcript_file)

        embed = EmbedBuilder.warning("Ticket Closing", "This channel will be deleted in 5 seconds...")
        await interaction.response.send_message(embed=embed)
        await discord.utils.sleep_until(discord.utils.utcnow() + datetime.timedelta(seconds=5))
        await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.success, emoji="✋", custom_id="maple_ticket_claim_btn")
    async def claim_ticket_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_staff(interaction):
            return await interaction.response.send_message("❌ Only staff members can claim tickets.", ephemeral=True)
        embed = EmbedBuilder.success("Ticket Claimed", f"This ticket has been claimed by {interaction.user.mention}.")
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Rename Channel", style=discord.ButtonStyle.secondary, emoji="✏️", custom_id="maple_ticket_rename_btn")
    async def rename_ticket_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.modals import TicketRenameModal
        await interaction.response.send_modal(TicketRenameModal())


class ApplicationLaunchView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Apply Now", style=discord.ButtonStyle.primary, emoji="📋", custom_id="maple_apply_now_btn")
    async def apply_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        from views.modals import ApplicationModal
        questions = [
            {"label": "Why do you wish to apply?", "placeholder": "Explain your background and goals...", "long": True},
            {"label": "What relevant experience do you have?", "placeholder": "Detail past staff/moderation roles...", "long": True},
            {"label": "Weekly Availability (Hours)", "placeholder": "e.g., 15-20 hours", "long": False}
        ]
        await interaction.response.send_modal(ApplicationModal(app_title="Staff Member Application", questions=questions))


class ApplicationReviewView(discord.ui.View):
    def __init__(self, app_id: int):
        super().__init__(timeout=None)
        self.app_id = app_id

    @discord.ui.button(label="Approve Application", style=discord.ButtonStyle.success, emoji="✅", custom_id="maple_app_approve_btn")
    async def approve_app(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ Only staff/moderators can review applications.", ephemeral=True)
        await db.update_application_status(self.app_id, "approved", interaction.user.id, "Approved by staff")
        embed = EmbedBuilder.success("Application Approved", f"Application **#{self.app_id}** approved by {interaction.user.mention}.")
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Reject Application", style=discord.ButtonStyle.danger, emoji="❌", custom_id="maple_app_reject_btn")
    async def reject_app(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_mod(interaction):
            return await interaction.response.send_message("❌ Only staff/moderators can review applications.", ephemeral=True)
        await db.update_application_status(self.app_id, "rejected", interaction.user.id, "Rejected by staff")
        embed = EmbedBuilder.error("Application Rejected", f"Application **#{self.app_id}** rejected by {interaction.user.mention}.")
        await interaction.response.send_message(embed=embed)
