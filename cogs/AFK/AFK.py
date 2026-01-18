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

from typing import Optional, TYPE_CHECKING

from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from utils.console import console
from utils.custom import MaiCog
from utils.constants import Colors, Emoji, Links, MAI

if TYPE_CHECKING:
    from mai import Mai

class AFK(
    MaiCog,
    name="AFK",
    description="Let People Know You're Away From Discord",
    emoji=Emoji.AFK,
):
    def __init__(self, bot: commands.Bot):
        self.bot: Mai = bot
        
    @commands.slash_command(name="afk", description="Go AFK")
    @commands.cooldown(1, 1, BucketType.user)
    async def afk(self, ctx: discord.ApplicationContext, message: str) -> None:
        if ctx.guild is None:
            return
        
        return
    
def setup(bot):
    bot.add_cog(AFK(bot))