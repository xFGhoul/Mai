"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import discord
from discord.ext import commands

from helpers.constants import *
from helpers.logging import log

from typing import Union

from db.models import Guild


class Developer(
    commands.Cog,
    command_attrs=dict(hidden=True),
):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(invoke_without_subcommand=False)
    @commands.is_owner()
    @commands.guild_only()
    async def blacklist(self, ctx: commands.Context):
        pass

    @blacklist.command(
        name="add",
        description="Blacklist A Server From Using Mai",
        brief="blacklist add 1234567\nblacklist add My Server Name",
    )
    async def add(
        self,
        ctx: commands.Context,
        guild: Union[discord.Guild, int],
        *,
        reason: str,
    ) -> None:
        if guild is None:
            await ctx.send_help(ctx.command)
            return

        guild_id = guild if type(guild) is int else guild.id
        guild = await Guild.get(discord_id=guild_id)

        if guild.is_bot_blacklisted:
            embed = discord.Embed(
                color=Colors.ERROR_COLOR,
                description=f"{Emoji.ERROR} Guild Already Blacklisted. refer to `-help blacklist remove`",
            )
            await ctx.send(embed=embed)
            return
        else:
            guild.blacklisted = True
            await guild.save(update_fields=["is_bot_blacklisted"])
            await guild.refresh_from_db(fields=["is_bot_blacklisted"])
            await Guild.create(blacklisted_reason=reason)
            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"`{Emoji.CHECKMARK_EMOJI} {guild.discord_id}` Has been successfully `blacklisted` for `{reason}`",
            )
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(Emoji.CHECKMARK_EMOJI)

    @blacklist.command(
        name="remove",
        description="Remove A Server Blacklist From Mai",
        brief="blacklist remove 1234567\nblacklist remove My Server Name",
    )
    async def remove(
        self, ctx: commands.Context, guild: Union[discord.Guild, int]
    ):

        if guild is None:
            await ctx.send_help(ctx.command)
            return

        guild_id = guild if type(guild) is int else guild.id
        guild = await Guild.get(discord_id=guild_id)

        if not guild.blacklisted:
            embed = discord.Embed(
                color=Colors.ERROR_COLOR,
                description=f"{Emoji.ERROR} Guild Not Blacklisted. refer to `-help blacklist add`",
            )
            await ctx.send(embed=embed)
            return
        else:
            guild.blacklisted = False
            await guild.save(update_fields=["blacklisted"])
            await guild.refresh_from_db(fields=["blacklisted"])
            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"`{Emoji.CHECKMARK_EMOJI} {guild.discord_id}` Has been successfully `blacklisted`",
            )
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(Emoji.CHECKMARK_EMOJI)

    @blacklist.command(
        name="list", description="List All Blacklisted Server ID's"
    )
    async def blacklist_list(self, ctx: commands.Context):
        guilds = await Guild.filter(discord_id=ctx.guild.id).all()
        for guild in guilds:
            g_blacklisted = []
            if guild.is_bot_blacklisted:
                g_blacklisted.append(guild.discord_id)
        blacklisted_ids = (
            ", ".join(g_blacklisted)
            if g_blacklisted is not None
            else "`No Blacklisted Servers`"
        )
        embed = discord.Embed(
            color=Colors.EMBED_COLOR,
            description=f"**Guild ID's:** {blacklisted_ids}",
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def createguild(self, ctx):
        await Guild.create(discord_id=ctx.guild.id)
        await ctx.send("ok done.")


def setup(bot):
    bot.add_cog(Developer(bot))
