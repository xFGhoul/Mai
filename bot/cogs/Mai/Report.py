"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import uuid
from typing import Union

import discord
from click import pass_context
from db.models import Reports
from discord.ext import commands
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class Report(
    Cog,
    name="Report",
    description="Report Guilds, Users, or Bugs About Mai",
    emoji=Emoji.REPORT,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="report",
        description="Report A Bug, User, or Guild",
        brief="report @Member doing illegal stuff\nreport bug ping doesn't work\nreport AGuildName doing illegal things",
    )
    async def report(
        self,
        ctx: commands.Context,
        kind: Union[str, discord.Member, discord.Guild],
        reason: str,
    ) -> None:
        if reason is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `reason` value needs to be passed",
            )
            await ctx.send(embed=embed, delete_after=15)
            return

        pass


def setup(bot):
    bot.add_cog(Report(bot))
