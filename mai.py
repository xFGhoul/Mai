import discord
import watchgod
import itertools
import os
import traceback

from typing import Tuple
from glob import glob

from discord.flags import MemberCacheFlags
from discord import Intents, AllowedMentions
from discord.ext import commands, tasks
from discord.ext.commands import AutoShardedBot

from tortoise import Tortoise
from tortoise.exceptions import IntegrityError

from db.tortoise.config import default
from db.models import Guild

from config.ext.config_parser import config

from locales.languages import *
from pycord18n.extension import I18nExtension, _

from utils.console import console
from utils.logging import log
from utils.constants import (
    EMBED_COLOR,
    SUCCESS_COLOR,
    CHECKMARK_EMOJI,
    ERROR_EMOJI,
    ERROR_COLOR,
)

from help_command import MaiHelpCommand


class Mai(AutoShardedBot):
    def __init__(self, *args, **kwargs):

        # Tuple of all activities the bot will display as a status
        self.activities = itertools.cycle(
            (
                discord.Activity(type=discord.ActivityType.watching, name="-help"),
                lambda: discord.Activity(
                    type=discord.ActivityType.listening,
                    name=f"{len(bot.commands)} Commands | {len(bot.users)} Users | {len(bot.guilds)} Servers",
                ),
            )
        )

        self.i18n = I18nExtension(
            [FRENCH, ENGLISH, JAPANESE, GERMAN, KOREAN, TURKISH, RUSSIAN], fallback="en"
        )

        # Declaring intents and initalizing parent class
        intents = Intents.all()
        stuff_to_cache = MemberCacheFlags.from_intents(intents)
        mentions = AllowedMentions(everyone=False, roles=False)
        super().__init__(
            intents=intents,
            command_prefix=self.determine_prefix,
            case_insensitive=True,
            help_command=MaiHelpCommand(),
            allowed_mentions=mentions,
            member_cache_flags=stuff_to_cache,
            chunk_guilds_at_startup=False,
            max_messages=1000,
            *args,
            **kwargs,
        )

        self.load_extensions()

    async def determine_prefix(
        self, bot: commands.Bot, message: discord.Message
    ) -> str:
        guild = message.guild
        if guild:
            guild_model, _ = await Guild.get_or_create(discord_id=guild.id)
            return commands.when_mentioned_or(guild_model.prefix)(bot, message)
        else:
            return commands.when_mentioned_or("!")(bot, message)

    async def get_locale(self, ctx: commands.Context) -> None:
        pass  # FIXME Overriding get_locale for pycordi18n but it's broken so just pass for now.

    def load_extensions(
        self, reraise_exceptions: bool = False
    ) -> Tuple[Tuple[str], Tuple[str]]:
        loaded_extensions = set()
        failed_extensions = set()
        for file in map(
            lambda file_path: file_path.replace(os.path.sep, ".")[:-3],
            glob("cogs/**/*.py", recursive=True),
        ):
            try:
                self.load_extension(file)
                loaded_extensions.add(file)
                log.info(
                    f"[bright_green][EXTENSION][/bright_green] [cyan1]{file} LOADED[/cyan1]"
                )
            except Exception as e:
                failed_extensions.add(file)
                log.info(
                    f"[bright red][EXTENSION ERROR][/bright red] [cyan1]FAILED TO LOAD COG {file}[/cyan1]"
                )
                if not reraise_exceptions:
                    traceback.print_exception(type(e), e, e.__traceback__)
                else:
                    raise e
        result = (tuple(loaded_extensions), tuple(failed_extensions))
        return result

    def _start(self) -> None:
        self.run(config["DISCORD_TOKEN"], reconnect=True)

    @tasks.loop(seconds=10)
    async def status(self):
        """Cycles through all status every 10 seconds"""
        new_activity = next(self.activities)
        # The commands one is callable so the command counts actually change
        if callable(new_activity):
            await self.change_presence(
                status=discord.Status.online, activity=new_activity()
            )
        else:
            await self.change_presence(
                status=discord.Status.online, activity=new_activity
            )

    @tasks.loop(seconds=1)
    async def cog_watcher_task(self) -> None:
        """Watches the cogs directory for changes and reloads files"""
        async for change in watchgod.awatch("cogs", watcher_cls=watchgod.PythonWatcher):
            for change_type, changed_file_path in change:
                try:
                    extension_name = changed_file_path.replace(os.path.sep, ".")[:-3]
                    if len(extension_name) > 36 and extension_name[-33] == ".":
                        continue
                    if change_type == watchgod.Change.modified:
                        try:
                            self.unload_extension(extension_name)
                        except commands.ExtensionNotLoaded:
                            pass
                        finally:
                            self.load_extension(extension_name)
                            log.info(
                                f"[bright_green][EXTENSION][/bright_green] [cyan1][AUTORELOADED] {extension_name}[/cyan1]"
                            )
                    else:
                        self.unload_extension(extension_name)
                        log.info(
                            f"[bright_red][EXTENSION][/bright_red] [cyan1][AUTOUNLOADED] {extension_name}[/cyan1]"
                        )
                except (commands.ExtensionFailed, commands.NoEntryPointError) as e:
                    traceback.print_exception(type(e), e, e.__traceback__)

    @status.before_loop
    async def before_status(self) -> None:
        """Ensures the bot is fully ready before starting the task"""
        await self.wait_until_ready()

    async def on_ready(self) -> None:
        """Called when we have successfully connected to a gateway"""
        await Tortoise.init(default.TORTOISE_CONFIG)
        # await self.i18n.init_bot(bot, self.get_locale(commands.Context)) #FIXME 'cahced_property' has no attribute 'id'. most likely due to how the pycordi18n uses pre_invoke, looking into it.

        console.print(
            "[cyan1]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/cyan1]"
        )
        console.print(
            """[cyan1]

    ███╗   ███╗ █████╗ ██╗    ██████╗  ██████╗ ████████╗      ██╗ ██████╗ 
    ████╗ ████║██╔══██╗██║    ██╔══██╗██╔═══██╗╚══██╔══╝     ██╔╝ ╚════██╗
    ██╔████╔██║███████║██║    ██████╔╝██║   ██║   ██║       ██╔╝   █████╔╝
    ██║╚██╔╝██║██╔══██║██║    ██╔══██╗██║   ██║   ██║       ╚██╗   ╚═══██╗
    ██║ ╚═╝ ██║██║  ██║██║    ██████╔╝╚██████╔╝   ██║        ╚██╗ ██████╔╝
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝    ╚═════╝  ╚═════╝    ╚═╝         ╚═╝ ╚═════╝ 
                                                                            
                                                                               
[/cyan1]"""
        )

        console.print(
            f"[cyan1]Signed into Discord as {self.user} (ID: {self.user.id}[/cyan1])\n"
        )
        console.print(f"[cyan1]Discord Version: {discord.__version__}[/cyan1]")
        console.print(
            "[cyan1]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/cyan1]"
        )
        self.status.start()
        self.cog_watcher_task.start()


# Defining root level commands
bot = Mai()


@bot.event
async def on_guild_join(guild: discord.Guild):
    try:
        await Guild.create(discord_id=guild.id, language="en")
    except IntegrityError:
        log.info(f"{guild.name} ({guild.id}) Has Reinvited Mai.")


# DEVELOPER ONLY COMMANDS :)


@bot.command()
@commands.is_owner()
async def load(ctx: commands.Context, extention: str) -> None:
    """Loads an extension, owners only"""
    bot.load_extension(f"cogs.{extention}")
    embed = discord.Embed(
        color=SUCCESS_COLOR,
        description=f"{CHECKMARK_EMOJI} {extention} Cog Has Loaded.",
    )
    await ctx.send(embed=embed)


@load.error
async def load_error(ctx: commands.Context, error) -> None:
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Can Only Be Used By The Bot's Owners.",
        )
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Extension Is Already Loaded.",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.ExtensionNotFound):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Extension Does Not Exist.",
        )
        await ctx.send(embed=embed)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.command()
@commands.is_owner()
async def unload(ctx: commands.Context, extention) -> None:
    """Unloads an extension, owners only"""
    bot.unload_extension(f"cogs.{extention}")
    embed = discord.Embed(
        color=SUCCESS_COLOR,
        description=f"{CHECKMARK_EMOJI} {extention} Cog Has Been Disabled.",
    )
    await ctx.send(embed=embed)


@unload.error
async def unload_error(ctx: commands.Context, error) -> None:
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Can Only Be Used By The Bot's Owners.",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.ExtensionNotLoaded):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Extension Is Not Loaded.",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.ExtensionNotFound):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Extension Does Not Exist.",
        )
        await ctx.send(embed=embed)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.command()
@commands.is_owner()
async def cogs(ctx: commands.Context) -> None:
    cogs = []

    for cog in bot.cogs:
        cogs.append(f"`{cog}`")

    cogs_str = ", ".join(cogs)
    embed = discord.Embed(title=f"All Cogs", description=cogs_str, colour=EMBED_COLOR)
    await ctx.send(embed=embed)


@cogs.error
async def cogs_error(ctx: commands.Context, error) -> None:
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Can Only Be Used By The Bot's Owners.",
        )
        await ctx.send(embed=embed)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.command()
@commands.is_owner()
async def reload(ctx: commands.Context, extension) -> None:
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    embed = discord.Embed(
        color=SUCCESS_COLOR,
        description=f"{CHECKMARK_EMOJI} Successfully Reloaded {extension}",
    )
    await ctx.send(embed=embed)


@reload.error
async def reload_error(ctx: commands.Context, error):
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Can Only Be Used By The Bot's Owners.",
        )
    elif isinstance(error, commands.ExtensionNotLoaded):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Extension Is Not Loaded.",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.ExtensionNotFound):
        embed = discord.Embed(
            color=ERROR_COLOR,
            description=f"{ERROR_EMOJI} This Extension Does Not Exist.",
        )
        await ctx.send(embed=embed)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)


if __name__ == "__main__":
    # Makes sure the bot only runs if this is run as main file
    try:
        bot._start()
    except Exception as e:
        log.exception(e)
