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
import humanize
import datetime

from typing import Optional

from discord.ext import commands
from discord.ext.commands import BucketType

from helpers.constants import *
from helpers.logging import log


from db.models import Guild, AFKModel


class AFK(
    commands.Cog,
    name="AFK",
    description="Let People Know You're Away From Discord",
):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )


def setup(bot):
    bot.add_cog(AFK(bot))
