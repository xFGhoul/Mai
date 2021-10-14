import time
import psutil
import platform

import discord
from discord.ext import commands

from db.models import Guild
from utils.constants import *
from utils.logging import log

from config.ext.config_parser import config


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
                url=BOT_SOURCE_CODE_URL,
            )
        )


class Misc(
    commands.Cog,
    name="Miscellaneous",
    description="Miscellaneous commands about Mai",
):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(name="invite", description="Get An Invite To The Bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def invite(self, ctx: commands.Context):
        await ctx.send(
            f"Here is your link {ctx.author.mention}!", view=Invite()
        )

    @commands.command(
        name="support", description="Get An Invite To The Bot Support Server"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def support(self, ctx: commands.Context):
        await ctx.send("Join The Support Server!", view=SupportServer())

    @commands.command(
        name="source", description="Get An Link To The Bot's Source Code"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def source(self, ctx: commands.Context):
        await ctx.send("Here is your link", view=Source())

    @commands.command(name="ping", description="pong")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
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

    @commands.command(name="info", description="Get bot stats")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def stats(self, ctx: commands.Context):

        loading_embed = discord.Embed(
            color=EMBED_COLOR,
            description=f"{LOADING_CIRCLE_EMOJI} Fetching Stats...",
        )
        message = await ctx.send(embed=loading_embed)

        embed = discord.Embed(title="Mai Information", color=EMBED_COLOR)

        developers = "Developers: `Ghoul#6066`, `sham#4810`"

        embed.add_field(
            name=f"{OWNER_EMOJI} Developers",
            value=f"{developers}",
            inline=False,
        )

        servers = f"{INFORMATION_EMOJI} Servers: `{len(self.bot.guilds)}`"
        users = f"{MENTION_EMOJI} Users: `{len(self.bot.users)}`"

        voice_channel_list = [
            len(guild.voice_channels) for guild in self.bot.guilds
        ]
        voice_channels = (
            f"{VOICE_CHANNEL_EMOJI} Voice Channels: `{sum(voice_channel_list)}`"
        )

        text_channels_list = [
            len(guild.text_channels) for guild in self.bot.guilds
        ]
        text_channels = (
            f"{CHANNEL_EMOJI} Text Channels: `{sum(text_channels_list)}`"
        )

        stage_channel_list = [
            len(guild.stage_channels) for guild in self.bot.guilds
        ]
        stage_channels = (
            f"{STAGE_EMOJI} Stage Channels: `{sum(stage_channel_list)}`"
        )

        commands = f"{SLASH_COMMAND} Commands: `{len(self.bot.commands)}`"

        embed.add_field(
            name=f"{STATS_EMOJI} Statistics",
            value=f"{servers}\n{users}\n{voice_channels}\n{text_channels}\n{stage_channels}\n{commands}",
            inline=False,
        )

        virtual_mem = psutil.virtual_memory()

        os = f"{WINDOWS_10_EMOJI} OS: `Windows`"
        cpu = f"{CPU_EMOJI} CPU: `{psutil.cpu_percent()}%`"
        ram = f"{RAM_EMOJI} RAM: `{virtual_mem.percent}%`"

        embed.add_field(
            name=f"{PC_EMOJI} PC", value=f"{os}\n{cpu}\n{ram}", inline=False
        )

        python = f"{PYTHON_EMOJI} Python: `{platform.python_version()}`"
        pycord = f"{PYCORD_EMOJI} Pycord: `{discord.__version__}`"
        mai_version = config["BOT_VERSION"]
        mai = f"{MAI_EMOJI} Mai: `{mai_version}`"

        embed.add_field(
            name=f"{STATS_EMOJI} Versions",
            value=f"{python}\n{pycord}\n{mai}",
            inline=False,
        )

        bot_invite = f"[Bot Invite]({BOT_INVITE_URL})"
        source_code = f"[Source Code]({BOT_SOURCE_CODE_URL})"
        support_server = f"[Support Server]({SUPPORT_SERVER_INVITE})"
        documentation = f"[Documentation]({BOT_DOCUMENTATION_URL})"
        embed.add_field(
            name=f"{LINK_EMOJI} Links",
            value=f"{bot_invite}\n{support_server}\n{source_code}\n{documentation}",
            inline=False,
        )

        embed.set_footer(text="Made With ❤️", icon_url=ctx.author.avatar.url)

        await message.edit(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
