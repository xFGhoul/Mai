"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from itertools import groupby

from discord import Embed

from db.models import ServerLogging
from .constants import *


def emoji(value: bool) -> str:
    """Convert a boolean value to an emoji

    Parameters
    ----------
    value : bool
        Value to represent

    Returns
    -------
    str
        Either a check mark or cross mark emoji
    """
    return Emoji.CHECKMARK if value else Emoji.ERROR


def format_setting(model: ServerLogging, setting: str) -> str:
    setting_title = (
        f"`{' '.join(setting.split('_')[1:]).replace('_', ' ').title()}`"
    )
    enabled = getattr(model, setting)
    return f"\t{setting_title}: {emoji(enabled)}"


def format_logging_model(model: ServerLogging) -> Embed:
    """Formats logging settings as an embed

    Parameters
    ----------
    model : ServerLogging
        Model retreived from a database

    Returns
    -------
    Embed
        Embed representing all settings of the logging system
    """
    embed = Embed(color=Colors.EMBED_COLOR)
    VALID_TYPES = {
        "channel_created",
        "channel_deleted",
        "channel_updated",
        "member_banned",
        "member_joined",
        "member_joined_voice_channel",
        "member_left",
        "member_left_voice_channel",
        "member_roles_changed",
        "member_unbanned",
        "member_updated",
        "message_deleted",
        "message_edited",
        "nickname_changed",
        "role_created",
        "role_deleted",
        "role_updated",
        "server_edited",
        "server_emojis_updated",
        "server_stickers_updated",
        "server_webhooks_updated",
        "invite_created",
        "invite_deleted",
        "stage_created",
        "stage_deleted",
        "stage_updated",
    }

    grouped = groupby(sorted(VALID_TYPES), key=lambda k: k.split("_")[0])
    for group_name, contents in grouped:
        group_title = group_name.title()
        settings = "\n".join(
            [format_setting(model, setting) for setting in contents]
        )
        embed.add_field(name=group_title, value=settings, inline=False)

    return embed
