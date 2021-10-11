import discord
import time


from discord.ext import commands

from utils.logging import log
from utils.constants import *

from db.models import Guild


class Invite(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(label="Invite the Bot!", url=BOT_INVITE_URL)
        )


class SupportServer(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(label="Support Server", url=SUPPORT_SERVER_INVITE)
        )


class Source(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(
                label="View The Source Code",
                url="https://github.com/xFGhoul/Mai",
            )
        )


class Misc(commands.Cog, name="Miscellaneous", description="XXX"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(name="invite", description="Get An Invite To The Bot")
    async def invite(self, ctx: commands.Context):
        await ctx.send(
            f"Here is your link {ctx.author.mention}!", view=Invite()
        )

    @commands.command(
        name="support", description="Get An Invite To The Bot Support Server"
    )
    async def support(self, ctx: commands.Context):
        await ctx.send("Join The Support Server!", view=SupportServer())

    @commands.command(
        name="source", description="Get An Link To The Bot's Source Code"
    )
    async def source(self, ctx: commands.Context):
        await ctx.send("Here is your link", view=Source())

    @commands.command(name="ping", description="pong")
    async def ping(self, ctx: commands.Context):
        before = time.monotonic()
        loading_embed = discord.Embed(
            color=EMBED_COLOR, description=f"{LOADING_CIRCLE_EMOJI} Pinging..."
        )
        message = await ctx.send(embed=loading_embed)
        ping = (time.monotonic() - before) * 1000
        pEmbed = discord.Embed(title="Stats:", color=EMBED_COLOR)
        pEmbed.add_field(name="Latency", value=f"{int(ping)}ms")
        pEmbed.add_field(
            name="API", value=f"{round(self.bot.latency * 1000)}ms"
        )
        db_time_start = time.time()
        guild = await Guild.get(discord_id=ctx.guild.id)
        db_time_end = time.time()
        db_time = db_time_end - db_time_start
        pEmbed.add_field(name="Database", value=f"{round(db_time * 1000)}ms")
        pEmbed.set_thumbnail(url=BOT_AVATAR_URL)
        pEmbed.set_footer(text="Developer: Ghoul#6066", icon_url=BOT_AVATAR_URL)
        await message.edit(content=None, embed=pEmbed)


def setup(bot):
    bot.add_cog(Misc(bot))
