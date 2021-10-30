import discord
import traceback

from typing import Optional, Union
from datetime import datetime

from discord.ext import commands
from discord.ext.commands import BucketType, Greedy
from discord import AuditLogAction, AuditLogEntry

from helpers.constants import *
from helpers.logging import log
from helpers.formatting import format_logging_model

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
        """Get The Logging Channel Of A Guild

        Parameters
        ----------
        guild : Union[discord.Guild, int]
            The Guild To Find The Channel For

        Returns
        -------
        [discord.TextChannel]
            The Logging Channel
        """
        guild_id = guild.id if type(guild) is discord.Guild else int(guild)

        guild_model = (await Guild.get_or_create(discord_id=guild_id))[0]

        logging = await ServerLogging.get(guild=guild_model)

        if logging.enabled:
            logging_channel_id = logging.channel_id

            text_channels = (
                self.bot.get_guild(guild).text_channels
                if type(guild) is int
                else guild.text_channels
            )

            loggging_channel = discord.utils.get(
                text_channels, id=logging_channel_id
            )
            return loggging_channel
        else:
            return

    async def get_logging_model(self, guild_id: int):
        """Get The Guild's Logging Model

        Parameters
        ----------
        guild_id : int
            ID of the Guild

        Returns
        -------
        [ServerLogging]
            The Specified Guild Model
        """
        guild = await Guild.get_or_none(discord_id=guild_id)

        logging = await ServerLogging.get(guild=guild)

        return logging

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
            color=Colors.EMBED_COLOR,
            description=f"**Logging Toggled To:** `{toggle}`",
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
            color=Colors.EMBED_COLOR,
            description=f"**Logging Channel Updated Too:** {channel.mention}",
        )

        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="view",
        description="View all enabled/disabled logs",
    )
    async def view(self, ctx: commands.Context):
        # loading_embed = discord.Embed(
        #     color=Colors.EMBED_COLOR,
        #     description=f"{Emoji.LOADING_CIRCLE} Fetching Stats...",
        # )
        # message = await ctx.send(embed=loading_embed)

        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        logging = await ServerLogging.get(guild=guild)
        await ctx.send(embed=format_logging_model(logging))

        # if logging.channel_id is not None:
        #     logging_channel = f"<#{logging.channel_id}>"
        # else:
        #     logging_channel = "`No Logging Channel`"

        # if logging.ignored_logging_channels is not None:
        #     for channel_id in logging.ignored_logging_channels:
        #         chan = f"<#{channel_id}>"

        #     ignored_channels = chan
        # else:
        #     ignored_channels = "`No Channels Ignored`"

        # embed = discord.Embed(
        #     color=Colors.EMBED_COLOR,
        #     description=f"**Logging Enabled:** `{logging.enabled}`\n**Ignore Log Actions By Bots:** `{logging.log_actions_by_bots}`\n**Logging Channel:** {logging_channel}\n**Ignored Channels:** {ignored_channels}",
        # )

        # embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        # embed.set_thumbnail(url=ctx.guild.icon.url)

        # embed.add_field(
        #     name=f"{Emoji.MESSAGES} Messages:",
        #     value=f"Message Edited: `{logging.message_edited}`\nMessage Deleted: `{logging.messaged_deleted}`",
        #     inline=False,
        # )

        # embed.add_field(
        #     name=f"{Emoji.MEMBERS} Members:",
        #     value=f"Nickname Changed: `{logging.nickname_changed}`\nMember Updated: `{logging.member_updated}`\nMember Banned: `{logging.member_banned}`\nMember Unbanned: `{logging.member_unbanned}`\nMember Joined: `{logging.member_joined}\n`Member Left: `{logging.member_left}`",
        #     inline=False,
        # )

        # embed.add_field(
        #     name=f"{Emoji.MENTION} Roles:",
        #     value=f"Role Created: `{logging.role_created}`\nRole Updated: `{logging.role_updated}`\nRole Deleted: `{logging.role_deleted}`\nMember Roles Updated: `{logging.member_roles_changed}`",
        #     inline=False,
        # )

        # embed.add_field(
        #     name=f"{Emoji.CHANNEL} Channels:",
        #     value=f"Channel Created: `{logging.channel_created}`\nChannel Updated: `{logging.channel_updated}`\nChannel Deleted: `{logging.channel_deleted}`",
        #     inline=False,
        # )

        # embed.add_field(
        #     name=f"{Emoji.VOICE_CHANNEL} Voice:",
        #     value=f"Member Joined VC: `{logging.member_joined_voice_channel}`\nMember Left VC: `{logging.member_left_voice_channel}`",
        #     inline=False,
        # )

        # embed.add_field(
        #     name=f"{Emoji.DISCORD_EMPLOYEE} Server:",
        #     value=f"Server Edited: `{logging.server_edited}`\nServer Emojis Updated: `{logging.server_emojis_updated}`",
        #     inline=False,
        # )
        # await message.edit(content=None, embed=embed)

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="set",
        aliases=["add"],
        description="Set Which Events Should Be Logged",
        brief="`logging set message_edited True`\n`logging set message_edited on`\n\n**All Possible Sets**\n`message_edited`\n`message_deleted`\n`nickname_changed`\n`member_updated`\n`member_banned`\n`member_unbanned`\n`member_joined`\n`member_left`\n`role_created`\n`role_updated`\n`role_deleted`\n`member_roles_changed`\n`member_joined_voice_channel`\n`member_left_voice_channel`\n`server_edit`\n`server_emojis_updated`\n`channel_created`\n`channel_updated`\n`channel_deleted`",
    )
    async def set(self, ctx: commands.Context, log: str, toggle: bool):

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
            "server_edited",
            "server_emojis_updated",
            "channel_created",
            "channel_updated",
            "channel_deleted",
        }

        if log not in VALID_TYPES:
            await ctx.send_help(ctx.command)

        else:
            guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

            logging = await ServerLogging.get(guild=guild)

            setattr(logging, log, toggle)

            await logging.save(update_fields=[log])
            await logging.refresh_from_db(fields=[log])

            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"{Emoji.CHECKMARK} `{log}` **Has Been Successfully Updated Too** `{toggle}`",
            )

            await ctx.send(embed=embed)

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
                color=Colors.ERROR_COLOR,
                description=f"{Emoji.ERROR} No Valid Channels Were Provided",
            )
            await ctx.send(embed=embed)
            return

        guild = await Guild.from_context(ctx)

        already_ignored_channels = []

        new_ignored_channels = []

        for channel in channels:
            ignored, exists = await ServerLogging.get_or_create(  # FIXME
                guild=guild, ignored_logging_channels=channel.id
            )
            if not exists:
                already_ignored_channels.append(channel)
            else:
                new_ignored_channels.append(channel)

        if already_ignored_channels:
            embed = discord.Embed(
                color=Colors.ERROR_COLOR,
                description=f"{', '.join([channel.mention for channel in already_ignored_channels])} Is Already Being Ignored.",
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            color=Colors.SUCCESS_COLOR,
            description=f"{', '.join([channel.mention for channel in new_ignored_channels])} Are Now Being Ignored.",
        )
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(Emoji.CHECKMARK_EMOJI)

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ):

        logging = await self.get_logging_model(guild_id=before.guild.id)

        if logging.message_edited is True and logging.enabled != False:

            member = before.author

            if member.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            if before.content == after.content:
                return

            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                timestamp=datetime.utcnow(),
                description=f":pencil: [Message]({before.jump_url}) Sent By {member.mention} Edited In {before.channel.mention}",
            )
            embed.set_author(name=str(member), icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Old Message", value=f"`{before.content}`")
            embed.add_field(name="New Message", value=f"`{after.content}`")
            log_channel = await self.get_logs_channel(before.guild.id)
            await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):

        logging = await self.get_logging_model(guild_id=message.guild.id)

        if logging.messaged_deleted is True and logging.enabled != False:

            member = message.author

            if member.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                timestamp=datetime.utcnow(),
                description=f":wastebasket: Message Sent By {member.mention} Deleted In {message.channel.mention}",
            )

            if message.content == "":
                return

            embed.set_author(name=str(member), icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Deleted Message", value=f"{message.content}")
            embed.set_footer(text=f"ID: {member.id} | Message ID: {message.id}")
            log_channel = await self.get_logs_channel(message.guild.id)
            await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        logging = await self.get_logging_model(member.guild.id)

        if logging.member_joined is True and logging.enabled != False:

            if member.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                timestamp=datetime.utcnow(),
                description=f":e_mail: {member.mention} Has Joined The Server",
            )
            embed.set_author(name=str(member), icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f"ID: {member.id}")
            log_channel = await self.get_logs_channel(member.guild.id)
            await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):

        logging = await self.get_logging_model(member.guild.id)

        if logging.member_left is True and logging.enabled != True:

            if member.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                timestamp=datetime.utcnow(),
                description=f"{member.mention} | {member.name}",
            )
            total_roles = [role.mention for role in member.roles]
            roles = total_roles[1:]
            roles = roles[::-1]
            embed.set_author(name="Member Left", icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Roles", value=" ".join(roles), inline=False)
            embed.set_footer(text=f"ID: {member.id}")
            log_channel = await self.get_logs_channel(member.guild.id)
            await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):

        return

        # FIXME: cannot get guild because discord.User has no guild, patch soon.

        logging = await self.get_logging_model(before.guild.id)

        if logging.member_updated is True and logging.enabled != False:

            if before.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            if before.avatar.url != after.avatar.url:
                embed = discord.Embed(
                    color=Colors.EMBED_COLOR,
                    timestamp=datetime.utcnow(),
                    description=f"{after.mention} **Updated Their Profile.**",
                )
                embed.set_author(name=after.name, icon_url=after.avatar.url)
                embed.set_thumbnail(url=after.avatar.url)
                embed.add_field(
                    name="Avatar",
                    value=f"[[before]]({before.avatar.url}) -> [[after]]({after.avatar.url})",
                )
                embed.set_footer(text=f"ID: {after.id}")
                log_channel = await self.get_logs_channel(before.guild.id)
                await log_channel.send(embed=embed)

            if before.name != after.name:
                embed = discord.Embed(
                    color=Colors.EMBED_COLOR,
                    timestamp=datetime.utcnow(),
                    description=f"{after.mention} **Updated Their Profile.**",
                )
                embed.set_author(name=after.name, icon_url=after.avatar.url)
                embed.set_thumbnail(url=after.avatar.url)
                embed.add_field(
                    name="Username",
                    value=f"**{before.name}** -> **{after.name}**",
                )
                embed.set_footer(text=f"ID: {after.id}")
                log_channel = await self.get_logs_channel()
                await log_channel.send(embed=embed)

            if before.discriminator != after.discriminator:
                embed = discord.Embed(
                    color=Colors.EMBED_COLOR,
                    timestamp=datetime.utcnow(),
                    description=f"{after.mention} **Updated Their Profile.**",
                )
                embed.set_author(name=after.name, icon_url=after.avatar.url)
                embed.set_thumbnail(url=after.avatar.url)
                embed.add_field(
                    name="Discriminator",
                    value=f"**#{before.discriminator}** -> **#{after.discriminator}**",
                )
                embed.set_footer(text=f"ID: {after.id}")
                log_channel = await self.get_logs_channel()
                await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ):

        logging = await self.get_logging_model(before.guild.id)

        if logging.member_updated is True and logging.enabled != False:

            if before.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            if before.nick != after.nick:
                try:
                    embed = discord.Embed(
                        color=Colors.EMBED_COLOR,
                        timestamp=datetime.utcnow(),
                        description=f":pencil: {after.mention} **Nickname Edited.**",
                    )
                    embed.set_author(name=after.name, icon_url=after.avatar.url)
                    embed.set_thumbnail(url=after.avatar.url)
                    embed.add_field(
                        name="Old Nickname", value=f"`{before.nick}`"
                    )
                    embed.add_field(
                        name="New Nickname", value=f"`{after.nick}`"
                    )
                    embed.set_footer(text=f"ID: {after.id}")
                    log_channel = await self.get_logs_channel()
                    await log_channel.send(embed=embed)
                except Exception as error:
                    traceback.print_exception(
                        type(error), error, error.__traceback__
                    )

        else:
            return


def setup(bot):
    bot.add_cog(Logging(bot))
