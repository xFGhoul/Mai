import discord

from typing import Optional, Union
from datetime import datetime

from discord.ext import commands
from discord.ext.commands import BucketType, Greedy
from discord import AuditLogAction, AuditLogEntry

from helpers.constants import *
from helpers.logging import log

from db.models import Guild, ServerLogging


class Logging(
    commands.Cog, name="Logging", description="Manage Server Logging"
):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    async def get_audit_log_entry(
        self,
        guild: discord.Guild,
        action: AuditLogAction,
        target: discord.abc.Snowflake,
    ) -> Optional[AuditLogEntry]:
        """Retreives an audity log entry that affected a specified entity.

        Parameters
        ----------
        guild : discord.Guild
            The guild to search logs for
        action : AuditLogAction
            The type of action to look for
        target : discord.abc.Snowflake
            The entity that was affected by this action

        Returns
        -------
        Optional[AuditLogEntry]
            The entry that was found or None if there is no entry matching requested conditions
        """
        entry = await guild.audit_logs(action=action).find(
            lambda entry: entry.target.id == target.id
        )
        return entry

    async def get_logs_channel(self, guild: Union[discord.Guild, int]):
        guild_id = guild.id if type(guild) is discord.Guild else int(guild)

        guild = await Guild.get_or_create(discord_id=guild_id)

        logging = await ServerLogging.get_or_none(guild=guild)

        if logging.enabled:
            logging_channel_id = logging.channel_id

            loggging_channel = discord.utils.get(
                guild.text_channels, id=logging_channel_id
            )
            return loggging_channel
        else:
            return

    @commands.group(
        invoke_without_subcommand=True, description="Manage Logging"
    )
    @commands.guild_only()
    async def logging(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            return

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="toggle",
        description="Toggle Logging on/off",
        brief="logging toggle on\nlogging toggle True",
    )
    async def toggle(self, ctx: commands.Context, toggle: bool):

        guild = await Guild.from_context(ctx)

        logging = await ServerLogging.get_or_none(guild=guild)

        logging.enabled = toggle
        await logging.save(update_fields=["enabled"])
        await logging.refresh_from_db(fields=["enabled"])

        embed = discord.Embed(
            color=EMBED_COLOR, description=f"**Logging Toggled To:** `{toggle}`"
        )

        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="channel",
        description="Set the channel used for logging",
        brief="logging channel 1234567\nlogging channel #channel(mention)",
    )
    async def channel(
        self, ctx: commands.Context, channel: Union[discord.TextChannel, int]
    ):
        channel_id = (
            channel.id if type(channel) is discord.TextChannel else int(channel)
        )

        guild = await Guild.from_context(ctx)

        logging = await ServerLogging.get_or_none(guild=guild)

        logging.channel_id = channel_id

        await logging.save(update_fields=["channel_id"])
        await logging.refresh_from_db(fields=["channel_id"])

        channel = ctx.guild.get_channel(channel_id)

        embed = discord.Embed(
            color=EMBED_COLOR,
            description=f"**Logging Channel Updated Too:** {channel.mention}",
        )

        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="view",
        description="View all enabled/disabled logs",
    )
    async def view(self, ctx: commands.Context):
        loading_embed = discord.Embed(
            color=EMBED_COLOR,
            description=f"{LOADING_CIRCLE_EMOJI} Fetching Stats...",
        )
        message = await ctx.send(embed=loading_embed)

        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        logging = await ServerLogging.get(guild=guild)

        if logging.channel_id is not None:
            logging_channel = f"<#{logging.channel_id}>"
        else:
            logging_channel = "`No Logging Channel`"

        if logging.ignored_logging_channels is not None:
            for channel_id in logging.ignored_logging_channels:
                chan = f"<#{channel_id}>"

            ignored_channels = chan
        else:
            ignored_channels = "`No Channels Ignored`"

        embed = discord.Embed(
            color=EMBED_COLOR,
            description=f"**Logging Enabled:** `{logging.enabled}`\n**Ignore Log Actions By Bots:** `{logging.log_actions_by_bots}`\n**Logging Channel:** {logging_channel}\n**Ignored Channels:** {ignored_channels}",
        )

        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_thumbnail(url=ctx.guild.icon.url)

        embed.add_field(
            name=f"{MESSAGES_EMOJI} Messages:",
            value=f"Message Edited: `{logging.message_edited}`\nMessage Deleted: `{logging.messaged_deleted}`",
            inline=False,
        )

        embed.add_field(
            name=f"{MEMBERS_EMOJI} Members:",
            value=f"Nickname Changed: `{logging.nickname_changed}`\nMember Updated: `{logging.member_updated}`\nMember Banned: `{logging.member_banned}`\nMember Unbanned: `{logging.member_unbanned}`\nMember Joined: `{logging.member_joined}\n`Member Left: `{logging.member_left}`",
            inline=False,
        )

        embed.add_field(
            name=f"{MENTION_EMOJI} Roles:",
            value=f"Role Created: `{logging.role_created}`\nRole Updated: `{logging.role_updated}`\nRole Deleted: `{logging.role_deleted}`\nMember Roles Updated: `{logging.member_roles_changed}`",
            inline=False,
        )

        embed.add_field(
            name=f"{CHANNEL_EMOJI} Channels:",
            value=f"Channel Created: `{logging.channel_created}`\nChannel Updated: `{logging.channel_updated}`\nChannel Deleted: `{logging.channel_deleted}`",
            inline=False,
        )

        embed.add_field(
            name=f"{VOICE_CHANNEL_EMOJI} Voice:",
            value=f"Member Joined VC: `{logging.member_joined_voice_channel}`\nMember Left VC: `{logging.member_left_voice_channel}`",
            inline=False,
        )

        embed.add_field(
            name=f"{EMPLOYEE_EMOJI} Server:",
            value=f"Server Edited: `{logging.server_edited}`\nServer Emojis Updated: `{logging.server_emojis_updated}`",
            inline=False,
        )
        await message.edit(content=None, embed=embed)

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="set",
        description="Set Which Events Should Be Logged",
        brief="`logging set message_edited True`\n`logging set message_edited on`\n\n**All Possible Sets**\n`message_edited`\n`message_deleted`\n`nickname_changed`\n`member_updated`\n`member_banned`\n`member_unbanned`\n`member_joined`\n`member_left`\n`role_created`\n`role_updated`\n`role_deleted`\n`member_roles_changed`\n`member_joined_voice_channel`\n`member_left_voice_channel`\n`server_edit`\n`server_emojis_updated`\n`channel_created`\n`channel_updated`\n`channel_deleted`",
    )
    async def set(self, ctx: commands.Context, log: str, toggle: bool):

        await ctx.send("Command Under Construction")
        return

        VALID_TYPES = {
            "message_edited",
            "message_deleted",
            "nickname_changed",
            "member_updated",
            "member_banned",
            "member_unbanned",
            "member_joined",
            "member_left",
            "role_created",
            "role_updated",
            "role_deleted",
            "member_roles_changed",
            "member_joined_voice_channel",
            "member_left_voice_channel",
            "server_edit",
            "server_emojis_updated",
            "channel_created",
            "channel_updated",
            "channel_deleted",
        }

        if log not in VALID_TYPES:
            await ctx.send_help(ctx.command)

        else:
            guild = await Guild.get_or_create(discord_id=ctx.guild.id)

            logging = await ServerLogging.get_or_none(guild=guild)

            # TODO

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="ignore",
        description="Set Channels To Be Ignored From Logging",
        brief="`logging ignore #mychannel`\n`logging ignore #mychannel1 #mychannel2 #mychannel3`",
    )
    async def ignore(
        self, ctx: commands.Context, channels: Greedy[discord.TextChannel]
    ):
        if not channels:
            embed = discord.Embed(
                color=ERROR_COLOR,
                description=f"{ERROR_EMOJI} No Valid Channels Were Provided",
            )
            await ctx.send(embed=embed)
            return

        guild = await Guild.from_context(ctx)

        already_ignored_channels = []

        new_ignored_channels = []

        for channel in channels:
            ignored, exists = await ServerLogging.get_or_create(
                guild=guild, ignored_logging_channels=channel.id
            )
            if not exists:
                already_ignored_channels.append(channel)
            else:
                new_ignored_channels.append(channel)

        if already_ignored_channels:
            embed = discord.Embed(
                color=ERROR_COLOR,
                description=f"{', '.join([channel.mention for channel in already_ignored_channels])} Is Already Being Ignored.",
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            color=SUCCESS_COLOR,
            description=f"{', '.join([channel.mention for channel in new_ignored_channels])} Are Now Being Ignored.",
        )
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(CHECKMARK_EMOJI)


def setup(bot):
    bot.add_cog(Logging(bot))
