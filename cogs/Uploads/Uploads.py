import discord
from discord.ext import commands

from utils.logging import log
from utils.constants import *


class Uploads(commands.Cog, name="Uploads", description="XXX"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} Ready.[/blue3]"
        )


def setup(bot):
    bot.add_cog(Uploads(bot))
