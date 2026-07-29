import discord
from discord.ext import commands
from aiohttp import web
import asyncio
import os
import sys
import time
import logging

import config
from database.database import db
from utils.embeds import EmbedBuilder
from views.buttons import TicketLaunchView, TicketControlView, ApplicationLaunchView, ApplicationReviewView

# Configure logger
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("MapleBot")

class MapleBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.guilds = True

        super().__init__(
            command_prefix="m!",
            intents=intents,
            help_command=None
        )

        self.start_time = time.time()

    async def start_health_server(self):
        """Web server endpoint allowing Render's Free Web Service tier to pass health checks."""
        try:
            app = web.Application()
            async def handle_ping(request):
                return web.Response(
                    text="Maple ManagementRx Bot is running and operational!",
                    status=200
                )

            app.router.add_get('/', handle_ping)
            app.router.add_get('/health', handle_ping)

            port = int(os.environ.get("PORT", 8080))
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", port)
            await site.start()
            logger.info(f"Render health check HTTP web server active on port {port}")
        except Exception as e:
            logger.error(f"Failed to start web health server: {e}")

    async def setup_hook(self):
        logger.info("Starting background health-check HTTP server for web deployment...")
        self.loop.create_task(self.start_health_server())

        logger.info("Initializing database schemas...")
        await db.init_db()

        # Register persistent UI Views so buttons work after bot restart
        self.add_view(TicketLaunchView())
        self.add_view(TicketControlView())
        self.add_view(ApplicationLaunchView())

        logger.info("Loading cogs...")
        cogs_list = [
            "cogs.utility",
            "cogs.moderation",
            "cogs.management",
            "cogs.tickets",
            "cogs.applications",
            "cogs.logging",
            "cogs.admin"
        ]

        for cog in cogs_list:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded extension: {cog}")
            except Exception as e:
                logger.error(f"Failed to load extension {cog}: {e}")

        logger.info("Syncing Slash Commands...")
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} application commands.")
        except Exception as e:
            logger.error(f"Failed to sync slash commands: {e}")

    async def on_ready(self):
        print(f"==================================================")
        print(f"  Maple ManagementRx v{config.BOT_VERSION} is online.")
        print(f"  Logged in as: {self.user} (ID: {self.user.id})")
        print(f"  Connected Guilds: {len(self.guilds)}")
        print(f"==================================================")

        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"over Maple ManagementRx v{config.BOT_VERSION}"
        )
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_app_command_error(self, interaction: discord.Interaction, error: Exception):
        """Global error handler for slash commands."""
        logger.error(f"Command Error in {interaction.command}: {error}", exc_info=error)
        
        if interaction.response.is_done():
            send_func = interaction.followup.send
        else:
            send_func = interaction.response.send_message

        if isinstance(error, discord.app_commands.MissingPermissions):
            embed = EmbedBuilder.error("Missing Permissions", "You do not have permission to run this command.")
            await send_func(embed=embed, ephemeral=True)
        elif isinstance(error, discord.app_commands.CommandOnCooldown):
            embed = EmbedBuilder.warning("Command Cooldown", f"Please wait `{round(error.retry_after, 1)}s` before reusing.")
            await send_func(embed=embed, ephemeral=True)
        else:
            embed = EmbedBuilder.error("Execution Error", "An error occurred while processing your request.")
            await send_func(embed=embed, ephemeral=True)

bot = MapleBot()
bot.tree.on_error = bot.on_app_command_error

def main():
    token = config.BOT_TOKEN
    print(">>> Checking environment variables...", flush=True)
    if not token or token == "your_discord_bot_token_here":
        print("CRITICAL ERROR: BOT_TOKEN is missing or not configured in environment variables!", flush=True)
        print("Please set BOT_TOKEN in your Pella Environment Variables / Secrets tab.", flush=True)
        sys.exit(1)

    print(">>> BOT_TOKEN found. Connecting to Discord gateway...", flush=True)
    bot.run(token)

if __name__ == "__main__":
    main()
