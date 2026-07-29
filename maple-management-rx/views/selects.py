import discord
from utils.embeds import EmbedBuilder
import config

class HelpCategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Utility Commands", value="utility", description="Ping, About, Help, Bot stats", emoji="🛠️"),
            discord.SelectOption(label="Moderation & Strikes", value="moderation", description="Warn, Kick, Ban, Timeout, Strikes, WKB", emoji="🛡️"),
            discord.SelectOption(label="Server Management", value="management", description="Config channels, roles, embed colors", emoji="⚙️"),
            discord.SelectOption(label="Ticket System", value="tickets", description="Create panel, handle support tickets", emoji="🎫"),
            discord.SelectOption(label="Application System", value="applications", description="Staff & Member application review", emoji="📋"),
            discord.SelectOption(label="Admin & Logging", value="admin", description="Server audit logging & permissions", emoji="🔐")
        ]
        super().__init__(placeholder="Select command category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        cat = self.values[0]
        if cat == "utility":
            embed = EmbedBuilder.default("Utility Commands", "Everyday bot status and inspection commands.")
            embed.add_field(name="/ping", value="Check bot websocket latency & API response times.", inline=False)
            embed.add_field(name="/about", value="Display Maple ManagementRx system info, server count & uptime.", inline=False)
            embed.add_field(name="/help", value="Interactive command documentation menu.", inline=False)
        elif cat == "moderation":
            embed = EmbedBuilder.default("Moderation & Strike Commands", "Enforce server rules with persistent logs.")
            embed.add_field(name="/warn <user> <reason>", value="Issue official warning to a member.", inline=False)
            embed.add_field(name="/warnings <user>", value="View warning history for a user.", inline=False)
            embed.add_field(name="/clearwarnings <user>", value="Clear warning history.", inline=False)
            embed.add_field(name="/strike <user> <reason>", value="Issue a strike according to Guild Strike Policy.", inline=False)
            embed.add_field(name="/strikes <user>", value="View active strike records.", inline=False)
            embed.add_field(name="/clearstrikes <user>", value="Clear user strike count.", inline=False)
            embed.add_field(name="/timeout <user> <duration> <reason>", value="Timeout/mute user (e.g., 10m, 2h, 1d).", inline=False)
            embed.add_field(name="/kick <user> [reason]", value="Kick member from server.", inline=False)
            embed.add_field(name="/ban <user> [reason]", value="Ban member from server.", inline=False)
            embed.add_field(name="/unban <user_id> [reason]", value="Unban member by ID.", inline=False)
        elif cat == "management":
            embed = EmbedBuilder.default("Server Management & Config", "Configure guild-specific settings.")
            embed.add_field(name="/config show", value="View current server configurations.", inline=False)
            embed.add_field(name="/config channels", value="Set log, moderation, and staff channels.", inline=False)
            embed.add_field(name="/config roles", value="Set staff, moderator, and admin roles.", inline=False)
            embed.add_field(name="/config color <hex>", value="Set custom embed color (e.g., #D97706).", inline=False)
        elif cat == "tickets":
            embed = EmbedBuilder.default("Ticket System Commands", "Manage support tickets seamlessly.")
            embed.add_field(name="/ticket panel", value="Deploy a persistent ticket creation panel.", inline=False)
            embed.add_field(name="/ticket close", value="Close current ticket & create transcript.", inline=False)
            embed.add_field(name="/ticket add <user>", value="Add member to ticket channel.", inline=False)
            embed.add_field(name="/ticket remove <user>", value="Remove member from ticket channel.", inline=False)
        elif cat == "applications":
            embed = EmbedBuilder.default("Application System Commands", "Custom applicant workflow.")
            embed.add_field(name="/apply panel", value="Deploy application button panel.", inline=False)
            embed.add_field(name="/apply setup", value="Configure application questions & channel.", inline=False)
        elif cat == "admin":
            embed = EmbedBuilder.default("Admin & Audit Controls", "High-level administrative oversight.")
            embed.add_field(name="/admin staff_list", value="View registered staff activity records.", inline=False)
            embed.add_field(name="/admin purge_logs", value="Purge old moderation logs.", inline=False)

        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(HelpCategorySelect())


class TicketCategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="General Support", value="General Support", description="Ask questions or get help with the server.", emoji="💬"),
            discord.SelectOption(label="Staff Support", value="Staff Support", description="Inquire about staff duties or assistances.", emoji="🛡️"),
            discord.SelectOption(label="Management / Report", value="Management Report", description="Escalate critical issues or report violations.", emoji="🚨"),
            discord.SelectOption(label="Other / Inquiries", value="Other", description="Miscellaneous ticket inquiries.", emoji="❓")
        ]
        super().__init__(placeholder="Select ticket category...", custom_id="ticket_category_select", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        from views.buttons import create_ticket_channel
        await create_ticket_channel(interaction, category)
