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
import datetime
import psutil
import aiohttp
import platform
import humanize
import time


from typing import Optional, TYPE_CHECKING

from discord.commands import SlashCommandGroup
from discord.ext import commands, pages

from sympy.core.symbol import var
from sympy.parsing.sympy_parser import (
    implicit_multiplication,
    parse_expr,
    standard_transformations,
)

from config.ext.parser import config
from utils.custom import MaiCog
from utils.constants import Colors, Emoji, Links, MAI, Char

if TYPE_CHECKING:
    from mai import Mai

class Miscellaneous(MaiCog, emoji=Emoji.MINECRAFT):
    def __init__(self, bot: commands.Bot):
        self.bot: Mai = bot

    @commands.slash_command(name="ping", description="pong!")  
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.trigger_typing()
        before = time.monotonic()
        loading_embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Emoji.LOADING_CIRCLE} Pinging...",
        )
        interaction = await ctx.respond(embed=loading_embed)

        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(color=Colors.DEFAULT)
        embed.add_field(name=f"{Emoji.MAI} Latency", value=f"{int(ping)}ms")
        embed.add_field(
            name=f"{Emoji.DISCORD} API",
            value=f"{round(self.bot.latency * 1000)}ms",
        )

        dbStart = time.time()
        await self.bot.db.fetchval("SELECT prefix FROM guild where discord_id = $1", ctx.guild.id)
        dbEnd = time.time()
        db = dbEnd - dbStart
        embed.add_field(
            name=f"{Emoji.POSTGRESQL} Database",
            value=f"{round(db * 1000)}ms",
        )

        rStart = time.time()
        await self.bot.cache.get(f"prefix:{ctx.guild}")
        rEnd = time.time()
        redis = rEnd - rStart
        embed.add_field(
            name=f"{Emoji.REDIS} Redis", value=f"{round(redis * 1000)}ms"
        )

        embed.set_thumbnail(url=Links.BOT_AVATAR_URL)
        embed.set_footer(text=MAI.DEVELOPER_FOOTER, icon_url=Links.BOT_AVATAR_URL)
        await interaction.edit_original_response(content=None, embed=embed)
        
    @commands.slash_command(
        name="uptime", description="Get Mai's Uptime"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def uptime(self, ctx: discord.ApplicationContext) -> None:
        await ctx.trigger_typing()
        now = datetime.datetime.utcnow()

        start_time = self.bot.uptime

        uptime = start_time - now

        humanized_uptime = humanize.precisedelta(
            uptime.total_seconds(), minimum_unit="milliseconds", format="%0.2f"
        )

        embed = discord.Embed(
            title="Bot Uptime",
            color=Colors.DEFAULT,
            description=f"{Char.ARROW} {humanized_uptime}",
        )

        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="info",
        description="Get bot stats",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def info(self, ctx: discord.ApplicationContext) -> None:

        await ctx.trigger_typing()

        loading_embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Emoji.LOADING_CIRCLE} Fetching Stats...",
        )
        message = await ctx.respond(embed=loading_embed)

        embed = discord.Embed(title="Mai Information", color=Colors.DEFAULT)

        embed.set_thumbnail(url=Links.BOT_AVATAR_URL)

        ghoul = ctx.guild.get_member(MAI.GHOUL_DISCORD_ID)
        nerd = ctx.guild.get_member(MAI.NERD_DISCORD_ID)

        if ctx.guild.id == MAI.SUPPORT_SERVER_ID:
            developers = f"Developers: {ghoul.mention}, {nerd.mention}"
        else:
            developers = f"Developers: `ghoul#1337`, `Nerd#4271`"

        embed.add_field(
            name=f"{Emoji.OWNER} Developers",
            value=f"{developers}",
            inline=False,
        )

        servers = f"{Emoji.INFORMATION} Servers: `{len(self.bot.guilds)}`"
        users = f"{Emoji.MENTION} Users: `{len(self.bot.users)}`"

        voice_channel_list = [len(guild.voice_channels) for guild in self.bot.guilds]
        voice_channels = (
            f"{Emoji.VOICE_CHANNEL} Voice Channels: `{sum(voice_channel_list)}`"
        )

        text_channels_list = [len(guild.text_channels) for guild in self.bot.guilds]
        text_channels = f"{Emoji.CHANNEL} Text Channels: `{sum(text_channels_list)}`"

        stage_channel_list = [len(guild.stage_channels) for guild in self.bot.guilds]
        stage_channels = (
            f"{Emoji.STAGE_CHANNEL} Stage Channels: `{sum(stage_channel_list)}`"
        )

        commands = f"{Emoji.SLASH_COMMAND} Commands: `{len(self.bot.commands)}`"

        embed.add_field(
            name=f"{Emoji.STATS} Statistics",
            value=f"{servers}\n{users}\n{voice_channels}\n{text_channels}\n{stage_channels}\n{commands}",
            inline=False,
        )

        virtual_mem = psutil.virtual_memory()

        os = f"{Emoji.WINDOWS_10} OS: `Windows`"
        cpu = f"{Emoji.CPU} CPU: `{psutil.cpu_percent()}%`"
        ram = f"{Emoji.RAM} RAM: `{virtual_mem.percent}%`"

        embed.add_field(
            name=f"{Emoji.PC} PC", value=f"{os}\n{cpu}\n{ram}", inline=False
        )

        python = f"{Emoji.PYTHON} Python: `{platform.python_version()}`"
        pycord = f"{Emoji.PYCORD} Pycord: `{discord.__version__}`"
        mai_version = config["BOT_VERSION"]
        mai = f"{Emoji.MAI} Mai: `{mai_version}`"

        embed.add_field(
            name=f"{Emoji.STATS} Versions",
            value=f"{python}\n{pycord}\n{mai}",
            inline=False,
        )

        bot_invite = f"[Bot Invite]({Links.BOT_INVITE_URL})"
        source_code = f"[Source Code]({Links.BOT_SOURCE_CODE_URL})"
        support_server = f"[Support Server]({Links.SUPPORT_SERVER_INVITE})"
        documentation = f"[Documentation]({Links.BOT_DOCUMENTATION_URL})"
        embed.add_field(
            name=f"{Emoji.LINK} Links",
            value=f"{bot_invite}\n{support_server}\n{source_code}\n{documentation}",
            inline=False,
        )

        embed.set_footer(text=MAI.DEVELOPER_FOOTER, icon_url=ctx.author.avatar.url)

        await message.edit_original_response(content=None, embed=embed)

    @commands.slash_command(
        name="math",
        description="Execute Math",
    )
    @commands.guild_only()
    async def math(
        self, ctx: discord.ApplicationContext, expression: str, *, vars: Optional[str]
    ) -> None:
        await ctx.trigger_typing()

        loading_embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Emoji.LOADING_CIRCLE} Calculating...",
        )
        message = await ctx.respond(embed=loading_embed)

        if vars is not None:
            declarations = vars.split(";")
            runtime_vars = dict()
            for declaration in declarations:
                lhs, rhs = tuple(declaration.split("="))
                runtime_vars.update({lhs: int(rhs)})
        else:
            runtime_vars = dict()

        result = parse_expr(
            expression,
            local_dict=runtime_vars,
            transformations=standard_transformations + (implicit_multiplication,),
        )
        embed = discord.Embed(
            title=f"Math Calculated {Emoji.BRAIN}",
            color=Colors.SUCCESS,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.add_field(name="Expression", value=expression, inline=False)
        var_mappings = "\n".join(
            [f"{var} -> {val}" for var, val in runtime_vars.items()]
        )
        if var_mappings:
            embed.add_field(name="Runtime variables", value=var_mappings, inline=False)
        embed.add_field(name="Result", value=result, inline=False)
        await message.edit_original_response(content=None, embed=embed)

    @commands.slash_command(
        name="avatar",
        description="Get Avatar of a User",
    )
    async def avatar(self, ctx: discord.ApplicationContext, user: discord.Member = None) -> None:
        if not user:
            user = ctx.author

        embed = discord.Embed(
            description=f"[[Open In Browser]({user.avatar.url})]",
            colour=Colors.DEFAULT,
        )
        embed.set_author(name=user, url=user.avatar.url, icon_url=user.avatar.url)
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="banner",
        description="Get Banner of User",
    )
    async def banner(self, ctx: discord.ApplicationContext, user: discord.Member = None) -> None:
        if not user:
            user = ctx.author

        user = await self.bot.fetch_user(user.id)

        if not user.banner:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {user.mention} has no banner!",
            )
            await ctx.respond(embed=embed)
            return

        if user.banner.is_animated():
            gif = user.banner.with_format("gif").url
            embed = discord.Embed(
                description=f"[[Open In Browser]({gif})]", color=Colors.DEFAULT
            )
            embed.set_image(url=gif)
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.respond(embed=embed)
        else:
            static = user.banner.with_format("png").url
            embed = discord.Embed(
                description=f"[[Open In Browser]({static})]",
                color=Colors.DEFAULT,
            )
            embed.set_image(url=static)
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.respond(embed=embed)

    @commands.slash_command(
        name="serverbanner",
        description="Get Server Banner",
    )
    @commands.guild_only()
    async def serverbanner(self, ctx: discord.ApplicationContext) -> None:
        if not ctx.guild.banner:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `{ctx.guild.name}` has no banner!",
            )
            await ctx.respond(embed=embed)
            return

        if ctx.guild.banner.is_animated():
            gif = ctx.guild.banner.with_format("gif").url
            embed = discord.Embed(
                description=f"[[Open In Browser]({gif})]", color=Colors.DEFAULT
            )
            embed.set_image(url=gif)
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.respond(embed=embed)
        else:
            static = ctx.guild.banner.with_format("png").url
            embed = discord.Embed(
                description=f"[[Open In Browser]({static})]",
                color=Colors.DEFAULT,
            )
            embed.set_image(url=static)
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.respond(embed=embed)

    @commands.slash_command(
        name="servericon",
        description="Get Server Icon",
    )
    @commands.guild_only()
    async def servericon(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            description=f"[[Open In Browser]({ctx.guild.icon.url})]",
            colour=Colors.DEFAULT,
        )
        embed.set_author(
            name=ctx.guild.name,
            url=ctx.guild.icon.url,
            icon_url=ctx.guild.icon.url,
        )
        embed.set_image(url=ctx.guild.icon.url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )

        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="screenshot",
        description="Take A Screenshot Of An Website",
    )
    @commands.guild_only()
    async def screenshot(
        self, ctx: discord.ApplicationContext, url: str, delay: Optional[int]
    ) -> None:
        if delay is None:
            delay = 1

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"[`{url}`]({url})",
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)

        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                params = {
                    "access_key": config["API_FLASH_TOKEN"],
                    "url": url,
                    "format": "jpeg",
                    "fresh": "true",
                    "quality": 100,
                    "delay": delay,
                    "response_type": "json",
                }
                async with session.get(
                    "https://api.apiflash.com/v1/urltoimage", params=params
                ) as response:

                    json = await response.json()
                    url = json["url"]

                    embed.set_image(url=url)
                    await ctx.respond(content=None, embed=embed)


    @commands.slash_command(name="cogs", description="List All Loaded Cogs")
    @commands.is_owner()
    async def cogs(self, ctx: discord.ApplicationContext) -> None:
        _pages = []
        
        cogs = self.bot.cogs
        for cog_name, cog_object in cogs.items():
            if cog_name == "Jishaku":
                cog_object.emoji = Emoji.PYCORD
            
            cog_emoji = cog_object.emoji if cog_object.emoji is not None else ""
            page = discord.Embed(title=f"{cog_emoji} {cog_object.qualified_name}", color=Colors.DEFAULT, description=f"{Emoji.WHITE_CHECKMARK} **{cog_object.description}**")
            page.set_footer(text=MAI.DEVELOPER_FOOTER, icon_url=Links.BOT_AVATAR_URL)
            page.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            page.set_thumbnail(url=ctx.author.avatar.url)
            page.set_image(url=MAI.DEVELOPER_IMAGE)
            _pages.append(page)
            
        paginator = pages.Paginator(pages=_pages, loop_pages=True, use_default_buttons=True, timeout=60)
        
        await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))