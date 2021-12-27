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

from db.models import Guild, GuildEvent


class Events(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_prefix_update(
        self,
        description: str,
        guild: discord.Guild,
        old_prefix: str,
        new_prefix: str,
        timestamp,
    ) -> None:
        guild = (await Guild.get_or_create(discord_id=guild.id))[0]

        await GuildEvent.create(
            guild=guild,
            description=description,
            old=old_prefix,
            new=new_prefix,
            timestamp=timestamp,
        )


def setup(bot):
    bot.add_cog(Events(bot))
