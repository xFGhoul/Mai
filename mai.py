"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import os
import sys

import glob
import discord
import jishaku
import watchfiles
import datetime
import traceback
import itertools

from typing import Tuple
from aiocache import Cache
from jeyyapi import JeyyAPIClient

from discord import Embed, Intents, AllowedMentions, MemberCacheFlags
from discord.ext import commands, tasks
from discord.ext.commands import AutoShardedBot

from discord.errors import ExtensionAlreadyLoaded, ExtensionNotFound, ExtensionFailed, ExtensionNotLoaded

from config.ext import config

from utils.database import MaiDB
from utils.console import console
from utils.logging import logger, discord_logger, setup_logger
from utils.exceptions import ValueNotPassed
from utils.constants import Links, Colors, Emoji, MAI
from utils.help import MaiHelpCommand

os.system("cls" if sys.platform == "win32" else "clear")

class Mai(AutoShardedBot):
    def __init__(self, development_mode: str = None, extension_dir: str = "cogs", *args, **kwargs,) -> None:
        if not development_mode:
            raise ValueNotPassed("__init__ expects development_mode to be provided but None was provided.")
        
        self.extension_dir: str = extension_dir
        self.development_mode: str = development_mode
        self.logger = logger
        self.discord_logger = discord_logger
        
        self.db: MaiDB = MaiDB()
        self.cache: Cache = Cache(Cache.REDIS, endpoint="127.0.0.1", port=6379, namespace="main")
        
        self.owners = config["BOT_OWNERS"]
        
        self.version = config["BOT_VERSION"]
        self.default_prefix = config["DEFAULT_PREFIX"]
        
        self.github: str = Links.BOT_SOURCE_CODE_URL
        self.support_server: str = Links.SUPPORT_SERVER_INVITE
        self.documentation: str = Links.BOT_DOCUMENTATION_URL
        self.invite_url: str = Links.BOT_INVITE_URL
        
        self.activities = itertools.cycle((discord.Activity(type=discord.ActivityType.watching, name="-help"), lambda: discord.Activity(type=discord.ActivityType.listening, name=f"{len(mai.all_commands)} Commands | {len(mai.users)} Users | {len(mai.guilds)} Servers")))
        
        self.uptime = datetime.datetime.utcnow()
        self.jeyy_api: JeyyAPIClient = JeyyAPIClient()
        
        intents: Intents = discord.Intents.default()
        intents.members = True
        intents.typing = False
        intents.presences = True
        intents.message_content = True
        
        super().__init__(
            intents=intents,
            command_prefix=self.determine_prefix,
            help_command=MaiHelpCommand(),
            case_insensitive = True,
            member_cache_flags=MemberCacheFlags.from_intents(intents),
            chunk_guilds_at_startup=False,
            allowed_mentions=AllowedMentions(everyone=False, roles=True),
            max_messages=2000,
            *args,
            **kwargs,
        )
        
        jishaku.Flags.NO_UNDERSCORE = True
        jishaku.Flags.RETAIN = True
        jishaku.Flags.HIDE = True
        self.load_extension("jishaku")
        self.load_extensions()
        
    async def cache_prefix(self, prefix: str, guild: discord.Guild) -> bool:
        if await self.cache.set(f"prefix:{guild.id}", prefix):
            return True
        else:
            return False

    async def get_cached_prefix(self, guild: discord.Guild) -> str:
        self.logger.info(f"Attempting To Fetch Cached Prefix For {guild.name} ({guild.id})")
        prefix = await self.cache.get(f"prefix:{guild.id}")
        return prefix
    
    async def determine_prefix(self, bot: AutoShardedBot, message: discord.Message) -> str:
        if not message.guild:
            return commands.when_mentioned_or(self.default_prefix)(bot, message)
        
        prefix = await self.get_cached_prefix(message.guild)
        if prefix and type(prefix) == str:
            prefix = prefix
            
        prefix = await self.db.fetchval("SELECT prefix FROM guild where discord_id = $1", message.guild.id)
        if prefix:
            if not await self.cache_prefix(prefix, message.guild):
                logger.error(f"Failed to cache prefix for {message.guild.name} ({message.guild.id})") # Cache Prefix Now That We Know It's In The Database
        else:
            await self.db.execute("INSERT INTO guild (discord_id, prefix) VALUES ($1, $2)", message.guild.id, self.default_prefix)
            if not await self.cache_prefix(self.default_prefix, message.guild):
                logger.error(f"Failed to cache prefix for {message.guild.name} ({message.guild.id})")
            prefix = self.default_prefix

        
        return commands.when_mentioned_or(prefix)(bot, message)
    
    def load_extensions(self, reraise_exceptions: bool = False) -> Tuple[Tuple[str, Tuple[str]]]:
        loaded_extensions = set()
        failed_extensions = set()
        for file in map(lambda file_path: file_path.replace(os.path.sep, ".")[:-3], 
                        glob.glob(f"{self.extension_dir}/**/*.py", recursive=True)):
            try:
                self.load_extension(file)
                loaded_extensions.add(file)
                logger.info(f"[EXTENSION] {file} LOADED")
                console.print(f"[bright_green][EXTENSION][/bright_green] [blue3]{file} LOADED[/blue3]")
            except Exception as e:
                failed_extensions.add(file)
                logger.info(f"[EXTENSION] FAILED TO LOAD COG {file}")
                console.print(f"[bright red][EXTENSION ERROR][/bright red] [blue3]FAILED TO LOAD COG {file}[/blue3]")
                if not reraise_exceptions:
                    traceback.print_exception(type(e), e, e.__traceback__)
                else:
                    raise e
        result = (tuple(loaded_extensions), tuple(failed_extensions))
        return result
    
    def _start(self) -> None:
        self.run(config["DISCORD_TOKEN"], reconnect=True)
    
    @tasks.loop(seconds=15)
    async def status(self) -> None:
        new_activity = next(self.activities)
        if callable(new_activity):
            await self.change_presence(status=discord.Status.streaming, activity=new_activity())
        else:
            await self.change_presence(status=discord.Status.online, activity=new_activity)
            
    @tasks.loop(seconds=1)
    async def cog_watcher_task(self) -> None:
        async for change in watchfiles.awatch(self.extension_dir):
            for change_type, changed_file_path in change:
                try:
                    extension_name: str = changed_file_path.replace(os.path.sep, ".")[:-3]
                    if len(extension_name) > 36 and extension_name[-33] == ".":
                        continue
                    splitted = extension_name.split(".")
                    cogs, folder_name, cog_name = splitted[-3], splitted[-2], splitted[-1]
                    new_extension = f"{cogs}.{folder_name}.{cog_name}"
                    if change_type == watchfiles.Change.modified:
                        try:
                            self.unload_extension(new_extension)
                        except ExtensionNotLoaded:
                            pass
                        finally:
                            self.load_extension(new_extension)
                            console.print(
                                f"[bright_green][EXTENSION][/bright_green] [blue3][AUTORELOADED] {new_extension}[/blue3]"
                            )
                    elif change_type == watchfiles.Change.added:
                        try:
                            self.load_extension(new_extension)
                            console.print(f"[bright_green][EXTENSION][/bright_green] [blue3][AUTOLOADED] {new_extension}[/blue3]")
                        except ExtensionFailed:
                            pass
                    elif change_type == watchfiles.Change.deleted:
                        try:
                            self.unload_extension(new_extension)
                            console.print(f"[bright_green][EXTENSION][/bright_green] [blue3][AUTOUNLOADED] {new_extension}[/blue3]")
                        except (ExtensionNotFound, ExtensionNotLoaded):
                            pass
                    else:
                        logger.error("Unknown Watchfiles Change Type")
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)

    async def on_ready(self) -> None:
        await self.db.initialize_pool(self.loop)
        console.print(
            "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
        )
        console.print(
            """[blue3]

    ███╗   ███╗ █████╗ ██╗    ██████╗  ██████╗ ████████╗      ██╗ ██████╗
    ████╗ ████║██╔══██╗██║    ██╔══██╗██╔═══██╗╚══██╔══╝     ██╔╝ ╚════██╗
    ██╔████╔██║███████║██║    ██████╔╝██║   ██║   ██║       ██╔╝   █████╔╝
    ██║╚██╔╝██║██╔══██║██║    ██╔══██╗██║   ██║   ██║       ╚██╗   ╚═══██╗
    ██║ ╚═╝ ██║██║  ██║██║    ██████╔╝╚██████╔╝   ██║        ╚██╗ ██████╔╝
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝    ╚═════╝  ╚═════╝    ╚═╝         ╚═╝ ╚═════╝


[/blue3]""",
            justify="full",
        )

        console.print(
            f"[blue3]Signed into Discord as {self.user} (ID: {self.user.id})[/blue3]\n"
        )
        console.print(f"[blue3]Discord Version: {discord.__version__}[/blue3]")
        console.print(f"[blue3]Bot Version: {self.version}[/blue3]")
        console.print(f"[blue3]Default Prefix: {self.default_prefix}[/blue3]")
        console.print(
            f"[blue3]Development Version: {self.development_mode}[/blue3]")
        console.print(
            "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
        )
        self.status.start()
        self.cog_watcher_task.start()
        
mai = Mai(development_mode="development")

@mai.check
async def is_guild_blacklisted(ctx: commands.Context) -> bool:
    blacklisted: bool = await mai.db.fetchval("SELECT is_bot_blacklisted FROM guild where discord_id = $1", ctx.guild.id)
    if blacklisted and ctx.author.id not in mai.owners:
        embed: Embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{ctx.author.mention}, {ctx.guild.name} Is Blacklisted From Using Mai For Breaking TOS."
        )
        await ctx.send(embed=embed)
        return False
    else:
        return True
    
if __name__ == "__main__":
    try:
        setup_logger()
        mai._start()
    except KeyboardInterrupt:
        logger.error("Bot Start Interrupted By User.")
        os._exit(1)