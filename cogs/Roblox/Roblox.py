import discord
from discord.ext import commands

from helpers.constants import *
from helpers.logging import log


class Roblox(commands.Cog, name="Roblox", description="XXX"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )


def setup(bot):
    bot.add_cog(Roblox(bot))
