import discord
import datetime
import humanize
import osutools

from ossapi import *

from discord.ext import commands
from discord.ext.commands import BucketType

from utils.logging import log
from utils.constants import *

from typing import Optional

from db.models import Guild, OSU

from config.ext.config_parser import config

osu_v1 = osutools.OsuClientV1(config["OSU_API_V1_KEY"])

osu_v2 = OssapiV2(
    config["OSU_API_V2_CLIENT_ID"],
    config["OSU_API_V2_CLIENT_SECRET"],
    config["OSU_API_V2_CLIENT_CALLBACK_URL"],
)


class StatsFlags(commands.FlagConverter, delimiter=" ", prefix="-"):
    d: Optional[str]  # Detailed


class Osu(commands.Cog, name="Osu!", description="Helpful osu! Commands."):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_db_username(self, ctx: commands.Context) -> str:
        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]
        osu_model = (
            await OSU.get_or_create(guild=guild, discord_id=ctx.author.id)
        )[0]
        username = osu_model.username
        return username

    async def parse_score(self, score: str):
        if score == "B":
            return B_EMOJI
        elif score == "F":
            return F_EMOJI
        elif score == "C":
            return C_EMOJI
        elif score == "A":
            return A_EMOJI
        elif score == "S":
            return S_EMOJI
        elif score == "SH":
            return SHD_EMOJI
        elif score == "XH":
            return SSHD_EMOJI
        else:
            return score

    async def parse_playstyle(self, user_playstyle: int):

        if user_playstyle == 1:
            playstyle = "mouse"
        elif user_playstyle == 2:
            playstyle = "keyboard"
        elif user_playstyle == 3:
            playstyle = "mouse, keyboard"
        elif user_playstyle == 5:
            playstyle = "mouse, tablet"
        elif user_playstyle == 6:
            playstyle = "keyboard, tablet"
        elif user_playstyle == 7:
            playstyle = "mouse, keyboard, tablet"
        elif user_playstyle == 8:
            playstyle = "tablet"
        elif user_playstyle == 9:
            playstyle = "mouse, touch"
        elif user_playstyle == 10:
            playstyle = "keyboard, touch"
        elif user_playstyle == 11:
            playstyle = "mouse, keyboard, touch"
        elif user_playstyle == 12:
            playstyle = "tablet, touch"
        elif user_playstyle == 15:
            playstyle = "mouse, keyboard, tablet, touch"
        else:
            playstyle = "None."

        return playstyle

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(
        invoke_without_subcommand=True, description="Manage Osu Commands"
    )
    @commands.guild_only()
    async def osu(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            return

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="link",
        aliases=["set"],
        description="Link your osu account to your discord account.",
        brief=f"-osu link Whitecat\n-osu set Whitecat",
    )
    async def osu_link(self, ctx: commands.Context, *, username: str):

        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        if await OSU.exists(guild=guild, discord_id=ctx.author.id):

            await OSU.filter(guild=guild, discord_id=ctx.author.id).update(
                username=username
            )

            embed = discord.Embed(
                color=EMBED_COLOR,
                description=f"{CHECKMARK_EMOJI} **Successfully updated username to `{username}`.**",
            )
            await ctx.send(embed=embed)
        else:
            await OSU.create(
                guild=guild, discord_id=ctx.author.id, username=username
            )
            embed = discord.Embed(
                color=EMBED_COLOR,
                description=f"{CHECKMARK_EMOJI} **Successfully created username `{username}`.**",
            )
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="stats",
        description="Get Basic Stats About A Player",
        brief="-osu stats Whitecat`\n`-osu stats Whitecat -d yes",
    )
    async def osu_stats(
        self,
        ctx: commands.Context,
        username: str,
        *,
        StatsFlags: StatsFlags,
    ):

        if username is None:
            username = await self.fetch_db_username(ctx)

        user_v1 = osu_v1.fetch_user(username=username)

        if user_v1 is None:
            embed = discord.Embed(
                color=ERROR_COLOR,
                description=f"{ERROR_EMOJI} **The user {username} was not found!**",
            )
            await ctx.send(embed=embed)
            return

        # NOTE: I run my own local version of osutools, so If you get an error from these two lines, change

        # osutools/user.py
        # seconds = int(user_info["total_seconds_played"])
        # self.playtime = Playtime(seconds)

        # CHANGES TO

        # seconds = int(user_info['total_seconds_played'])
        # self.playtime = seconds

        delta = datetime.timedelta(seconds=user_v1.playtime)
        playtime = humanize.precisedelta(
            delta, suppress=["days"], minimum_unit="hours", format="%0.0f"
        )

        # DISCLAIMER: This Embed Style Has Been Recreated/Copied From https://github.com/AznStevy/owo-bot/, All Credits Goes To Him.

        if StatsFlags.d == None:

            user_v2 = osu_v2.user(username)

            embed = discord.Embed(
                color=EMBED_COLOR,
                description=f"▸ **Bancho Rank:** #{humanize.intcomma(user_v1.rank)} ({user_v1.country}#{humanize.intcomma(user_v1.country_rank)})\n▸ **Level:** {user_v1.level}%\n▸ **PP:** {humanize.intcomma(user_v1.pp)} **Acc:** {round(user_v1.accuracy, 2)}%\n▸ **Playcount:** {humanize.intcomma(user_v1.play_count)} ({playtime})\n▸ **Ranks:** {SSHD_EMOJI}`{user_v1.ssh_count}`{SS_EMOJI}`{user_v1.ss_count}`{S_EMOJI}`{user_v1.s_count}`{A_EMOJI}`{user_v1.a_count}`\n▸ **Ranked Score:** {humanize.intcomma(user_v1.ranked_score)}\n▸ **Total Score:** {humanize.intcomma(user_v1.total_score)}\n▸ **Total Hits:** {humanize.intcomma(user_v1.num_300 + user_v1.num_100 + user_v1.num_50)}\n▸ **Max Combo:** {humanize.intcomma(user_v2.statistics.maximum_combo)}",
            )

            if user_v2.twitter is None:
                twitter = "No Twitter."
            else:
                twitter = f"[{user_v2.twitter}]({user_v2.twitter})"

            if user_v2.discord is None:
                osu_discord = "No Discord."
            else:
                osu_discord = user_v2.discord

            embed.add_field(
                name="Contact",
                value=f"▸ **Discord:** {osu_discord} \n▸ **Twitter:** {twitter}",
                inline=False,
            )

            embed.add_field(
                name="Extra Info",
                value=f"▸ **Previously Known As:** {' , '.join(user_v2.previous_usernames)}  \n▸ **Playstyle:**: {await self.parse_playstyle(user_v2.playstyle)} \n▸ **Followers:** {humanize.intcomma(user_v2.follower_count)} \n▸ **Ranked/Approved Beatmaps:** {humanize.intcomma(user_v2.ranked_and_approved_beatmapset_count)} \n▸ **Replays Watched By Others:** {humanize.intcomma(user_v2.statistics.replays_watched_by_others)}",
                inline=False,
            )

            embed.set_author(
                name=f"Osu Standard Profile for {user_v1.username}",
                url=f"https://osu.ppy.sh/users/{user_v1.id}",
                icon_url=f"https://osu.ppy.sh/images/flags/{user_v1.country}.png",
            )
            embed.set_thumbnail(url=user_v1.avatar_url)
            embed.set_image(url=user_v2.cover_url)

            embed.set_footer(
                text=f"On osu! Bancho | User ID: {user_v1.id}",
                icon_url=OSU_LOGO_IMAGE,
            )

            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(
                color=EMBED_COLOR,
                description=f"▸ **Bancho Rank:** #{humanize.intcomma(user_v1.rank)} ({user_v1.country}#{humanize.intcomma(user_v1.country_rank)})\n▸ **Level:** {user_v1.level}%\n▸ **PP:** {humanize.intcomma(user_v1.pp)} **Acc:** {round(user_v1.accuracy, 2)}%\n▸ **Playcount:** {humanize.intcomma(user_v1.play_count)} ({playtime})\n▸ **Ranks:** {SSHD_EMOJI}`{user_v1.ssh_count}`{SS_EMOJI}`{user_v1.ss_count}`{S_EMOJI}`{user_v1.s_count}`{A_EMOJI}`{user_v1.a_count}`",
            )
            embed.set_author(
                name=f"Osu Standard Profile for {user_v1.username}",
                url=f"https://osu.ppy.sh/users/{user_v1.id}",
                icon_url=f"https://osu.ppy.sh/images/flags/{user_v1.country}.png",
            )
            embed.set_thumbnail(url=user_v1.avatar_url)

            embed.set_footer(
                text=f"On osu! Bancho | User ID: {user_v1.id}",
                icon_url=OSU_LOGO_IMAGE,
            )

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="avatar",
        aliases=["av"],
        description="Get The Avatar Of A User",
        brief=f"-osu avatar\n-osu avatar Whitecat\n-osu av Whitecat",
    )
    async def osu_avatar(
        self, ctx: commands.Context, *, username: Optional[str]
    ):

        if username is None:
            username = await self.fetch_db_username(ctx)

        user = osu_v1.fetch_user(username=username)

        embed = discord.Embed(color=EMBED_COLOR)
        embed.set_author(
            name=f"{user}",
            url=f"https://osu.ppy.sh/users/{user.id}",
            icon_url=f"https://osu.ppy.sh/images/flags/{user.country}.png",
        )
        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
