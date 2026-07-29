import discord
from discord.ext import commands
from database.database import db
from utils.embeds import EmbedBuilder

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int):
        settings = await db.get_guild_settings(guild_id)
        channel_id = settings.get("log_channel_id")
        if channel_id:
            guild = self.bot.get_guild(guild_id)
            if guild:
                return guild.get_channel(channel_id)
        return None

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        chan = await self.get_log_channel(message.guild.id)
        if chan:
            embed = EmbedBuilder.warning(
                "Message Deleted",
                f"**Author:** {message.author.mention} (`{message.author.id}`)\n**Channel:** {message.channel.mention}"
            )
            embed.add_field(name="Content", value=message.content[:1000] or "*[No text content]*", inline=False)
            await chan.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot or not before.guild or before.content == after.content:
            return
        chan = await self.get_log_channel(before.guild.id)
        if chan:
            embed = EmbedBuilder.default(
                "Message Edited",
                f"**Author:** {before.author.mention} (`{before.author.id}`)\n**Channel:** {before.channel.mention}"
            )
            embed.add_field(name="Before", value=before.content[:500] or "*[Empty]*", inline=False)
            embed.add_field(name="After", value=after.content[:500] or "*[Empty]*", inline=False)
            await chan.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        chan = await self.get_log_channel(member.guild.id)
        if chan:
            embed = EmbedBuilder.success(
                "Member Joined",
                f"{member.mention} (`{member.name}`) joined the server.\n**Account Created:** {member.created_at.strftime('%Y-%m-%d')}"
            )
            await chan.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        chan = await self.get_log_channel(member.guild.id)
        if chan:
            embed = EmbedBuilder.warning(
                "Member Left",
                f"{member.mention} (`{member.name}`) left or was removed from the server."
            )
            await chan.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))
