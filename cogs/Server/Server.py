import discord

from discord.ext import commands

from typing import Optional

from helpers.constants import *
from helpers.logging import log

from db.models import Guild

from config.ext.config_parser import config


class Server(
    commands.Cog,
    name="Server Management",
    description="Manage how Mai interacts with your server",
):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(
        invoke_without_command=True, description="Manage Server Prefix"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    async def prefix(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            guild = await Guild.c_get_or_none_by_discord_id(ctx.guild.id)
            prefix = guild.prefix
            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"{ctx.author.mention}, My current prefix is `{prefix}` or {self.bot.user.mention}",
            )
            await ctx.send(embed=embed)

    @prefix.command(
        name="set",
        description="set the server prefix for mai",
        brief="prefix set !\nprefix set $$",
    )
    @commands.has_permissions(administrator=True)
    async def set(self, ctx: commands.Context, prefix: Optional[str]):

        if prefix == None:
            embed = discord.Embed(
                color=Colors.ERROR_COLOR,
                description=f"{Emoji.ERROR} Please Provide a Prefix.",
            )
            await ctx.send(embed=embed, delete_after=15)
            return

        guild = await Guild.c_get_or_none_by_discord_id(ctx.guild.id)

        if prefix == guild.prefix:
            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"My prefix for `{ctx.guild.name}` is already `{prefix}`!",
            )
            await ctx.send(embed=embed)
            return

        if guild is not None:
            guild.prefix = prefix
            await guild.c_save(update_fields=["prefix"])

            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"I set your guild's prefix to `{guild.prefix}`",
            )
            await ctx.send(embed=embed)
        else:
            await Guild.create(
                discord_id=ctx.guild.id, prefix=prefix, language="en"
            )
            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"I set your guild's prefix to `{guild.prefix}`",
            )
            await ctx.send(embed=embed)

    @prefix.command(
        name="reset",
        description="set the server prefix for mai",
        brief="prefix reset",
    )
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx: commands.Context):

        guild = await Guild.c_get_or_none_by_discord_id(ctx.guild.id)
        if guild is not None:
            guild.prefix = config["DEFAULT_PREFIX"]
            await guild.c_save(update_fields=["prefix"])
            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"I resetted this guild's prefix to `{guild.prefix}`",
            )
            await ctx.send(embed=embed)
        else:
            await Guild.create(
                discord_id=ctx.guild.id, prefix="-", language="en"
            )
            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description="Prefix Resetted to default.",
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Server(bot))
