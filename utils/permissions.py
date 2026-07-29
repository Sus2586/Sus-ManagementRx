import discord
from database.database import db

async def is_admin(interaction: discord.Interaction) -> bool:
    """Checks if user has Administrator permission or configured Admin role."""
    if interaction.user.guild_permissions.administrator:
        return True
    
    settings = await db.get_guild_settings(interaction.guild_id)
    admin_role_id = settings.get("admin_role_id")
    if admin_role_id:
        role_ids = [r.id for r in interaction.user.roles]
        if admin_role_id in role_ids:
            return True
    return False

async def is_mod(interaction: discord.Interaction) -> bool:
    """Checks if user has Manage Messages / Moderate Members permission or Mod role."""
    if interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.moderate_members:
        return True
    
    settings = await db.get_guild_settings(interaction.guild_id)
    mod_role_id = settings.get("mod_role_id")
    admin_role_id = settings.get("admin_role_id")
    role_ids = [r.id for r in interaction.user.roles]
    if (mod_role_id and mod_role_id in role_ids) or (admin_role_id and admin_role_id in role_ids):
        return True
    return False

async def is_staff(interaction: discord.Interaction) -> bool:
    """Checks if user is staff member."""
    if await is_mod(interaction):
        return True
    settings = await db.get_guild_settings(interaction.guild_id)
    staff_role_id = settings.get("staff_role_id")
    if staff_role_id:
        role_ids = [r.id for r in interaction.user.roles]
        if staff_role_id in role_ids:
            return True
    return False

def can_moderate(moderator: discord.Member, target: discord.Member) -> bool:
    """Prevents moderators from acting against users with equal or higher top role."""
    if moderator.id == moderator.guild.owner_id:
        return True
    if target.id == moderator.guild.owner_id:
        return False
    return moderator.top_role.position > target.top_role.position
