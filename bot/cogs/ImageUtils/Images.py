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
import aiohttp

from typing import Optional
from discord.ext import commands

from jeyyapi import JeyyAPIClient
from asyncdagpi import Client as DagpiClient
from asyncdagpi import ImageFeatures

from helpers.constants import *
from helpers.logging import log

from config.ext.parser import config


class ImageUtils(
    commands.Cog, name="Image Utils", description="Funny Image Utilities"
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.jeyyapi_client = JeyyAPIClient(session=self.bot.session)
        self.dagpi_client = DagpiClient(
            config["DAGPI_API_KEY"], session=self.bot.session
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="triggered",
        description="Return Triggered Image Of Someones Avatar",
        brief="triggered (works with no mention)\ntriggered @Member",
    )
    async def triggered(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                avatar = member.avatar.with_static_format("png")
                async with session.get(
                    f'https://some-random-api.ml/canvas/triggered?avatar={avatar}&key={config["SOME_RANDOM_API_KEY"]}'
                ) as resp:
                    await ctx.send(resp.url)

    @commands.command(
        name="wanted",
        description="Return Wanted Image Of Someones Avatar",
        brief="wanted @Member\nwanted (works with no mention)",
    )
    async def wanted(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        member_avatar_url = member.avatar.replace(
            format="png", static_format="png"
        )

        image = await self.dagpi_client.image_process(
            ImageFeatures.wanted(), member_avatar_url.url
        )

        file = discord.File(fp=image.image, filename=f"wanted.{image.format}")

        await ctx.send(file=file)

    @commands.command(
        name="bonk",
        description="Return Bonk Image Of Someones Avatar",
        brief="bonk @Member\nbonk",
    )
    async def bonk(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        member_avatar_url = member.avatar.replace(
            format="png", static_format="png"
        ).url

        image = await self.jeyyapi_client.bonks(member_avatar_url)

        file = discord.File(fp=image, filename=f"{member.name}-bonks.gif")

        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(ImageUtils(bot))
