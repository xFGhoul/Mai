import discord
from discord.ext import commands

from utils.logging import log
from utils.constants import *


class Captcha(commands.Cog, name="Captcha", description="XXX"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][cyan1] {type(self).__name__} Ready.[/cyan1]"
        )


def setup(bot):
    bot.add_cog(Captcha(bot))
