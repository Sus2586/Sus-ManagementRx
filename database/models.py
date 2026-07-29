from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class GuildConfig:
    guild_id: int
    log_channel_id: Optional[int] = None
    mod_channel_id: Optional[int] = None
    staff_channel_id: Optional[int] = None
    ticket_category_id: Optional[int] = None
    application_category_id: Optional[int] = None
    staff_role_id: Optional[int] = None
    mod_role_id: Optional[int] = None
    admin_role_id: Optional[int] = None
    embed_color: str = "0xD97706"
    wkb_enabled: bool = True
    strike_1_action: str = "Warning / Reminder"
    strike_2_action: str = "Temporary Mute / Timeout (24h)"
    strike_3_action: str = "Kick / Ban Escalation"

@dataclass
class ModerationRecord:
    id: int
    guild_id: int
    target_id: int
    target_name: str
    moderator_id: int
    moderator_name: str
    action_type: str
    reason: str
    timestamp: str

@dataclass
class StrikeRecord:
    id: int
    guild_id: int
    target_id: int
    strike_number: int
    moderator_id: int
    reason: str
    action_taken: str
    timestamp: str

@dataclass
class TicketRecord:
    id: int
    guild_id: int
    ticket_channel_id: int
    user_id: int
    category: str
    status: str
    created_at: str
    closed_at: Optional[str] = None
    closed_by: Optional[int] = None
