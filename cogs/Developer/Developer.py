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
import traceback
import inspect

from typing import TYPE_CHECKING, Optional

from discord import Embed
from discord import ExtensionAlreadyLoaded, ExtensionNotFound, ExtensionNotLoaded
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from utils.console import console
from utils.custom import MaiCog
from utils.constants import Colors, Emoji, Links, MAI

if TYPE_CHECKING:
    from mai import Mai

class AFK(
    MaiCog,
    name="Developer",
    description="Developer Settings",
    emoji=Emoji.DEVELOPER,
):
    def __init__(self, bot: commands.Bot):
        self.bot: Mai = bot
        
    dev = SlashCommandGroup("dev", "Manage Dev Settings")
    
    cogs = dev.create_subgroup("cogs", "Manage Cogs")
    
    @dev.command(name="which", description="Find The Cog A Command Is From")
    @commands.is_owner()
    async def which(self, ctx: discord.ApplicationContext, *, command_name: str) -> None:
        command = self.bot.get_application_command(command_name)
        if command is None:
            embed: Embed = discord.Embed(
                description=f"{Emoji.ERROR} `{command_name}` **does not exist.**",
                color=Colors.ERROR,
            )
        else:
            inner_command = command.callback
            command_defined_on: int = inspect.getsourcelines(inner_command)[1]
            full_command_signature: str = (
                f"`async def {inner_command.__name__}{inspect.signature(inner_command)} -> None:`"
            )
            embed: Embed = discord.Embed(
                title="Target Acquired \U0001F3AF", color=Colors.SUCCESS
            )
            embed.add_field(
                name="Part of Extension",
                value=f"`{command.cog.qualified_name}`"
                if command.cog is not None
                else "`Root Module`",
                inline=False,
            )
            embed.add_field(name="Source File", value=f"`{inspect.getsourcefile(inner_command)[-7:]}`", inline=False)
            embed.add_field(
                name="Defined on line",
                value=f"`{command_defined_on}`",
                inline=False,
            )
            embed.add_field(
                name="Signature",
                value=full_command_signature,
                inline=False)
        await ctx.respond(embed=embed)
        
    @cogs.command(name="load", description="Load Cog")
    @commands.is_owner()
    async def load(self, ctx: discord.ApplicationContext, *, extentions: Optional[str]) -> None:
        if self.bot.development_mode != "development":
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `bot.development_mode` set to `{self.bot.development_mode}`, commands such as `load`, `reload` and `unload` require `bot.development_mode` to be **development**",
            )
            await ctx.respond(embed=embed)
            return

        if extentions is None:
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `extention` argument missing",
            )
            await ctx.respond(embed=embed)
            return
        
        embed: Embed = discord.Embed(color=Colors.DEFAULT, description=f"{Emoji.LOADING_DOTS} Loading Extensions...")
        interaction = await ctx.respond(content=None, embed=embed)

        loaded_extensions = []

        for extension in extentions.split(" "):
            self.bot.load_extension(f"cogs.{extension}.{extension}")
            loaded_extensions.append(f"`{extension}`")

        embed: Embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.WHITE_CHECKMARK} {', '.join(loaded_extensions)} Are Now Loaded!",
        )

        await interaction.edit_original_response(embed=embed)
        
    @load.error
    async def load_error(self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError) -> None:
        if isinstance(error, commands.NotOwner):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Can Only Be Used By The Bot's Owners.",
            )
            await ctx.respond(embed=embed)
        elif isinstance(error, ExtensionAlreadyLoaded):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Extension Is Already Loaded.",
            )
            await ctx.respond(embed=embed)
        elif isinstance(error, ExtensionNotFound):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Extension Does Not Exist.",
            )
            await ctx.respond(embed=embed)
        else:
            traceback.print_exception(type(error), error, error.__traceback__)


    @cogs.command(name="unload", description="Unload An Cog")
    @commands.is_owner()
    async def unload(self, ctx: discord.ApplicationContext, *, extentions: Optional[str]) -> None:
        if self.bot.development_mode != "development":
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `bot.development_mode` set to `{self.bot.development_mode}`, commands such as `load`, `reload` and `unload` require `bot.development_mode` to be **development**",
            )
            await ctx.respond(embed=embed)
            return

        if extentions is None:
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `extensions` argument missing",
            )
            await ctx.respond(embed=embed)
            return
        
        embed: Embed = discord.Embed(color=Colors.DEFAULT, description=f"{Emoji.LOADING_DOTS} Unloading Extensions...")
        interaction = await ctx.respond(content=None, embed=embed)

        unloaded_extensions = []

        for extention in extentions.split(" "):
            self.bot.unload_extension(f"cogs.{extention}.{extention}")
            unloaded_extensions.append(f"`{extention}`")

        embed: Embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.WHITE_CHECKMARK} {', '.join(unloaded_extensions)} Are Now Unloaded!",
        )

        await interaction.edit_original_response(content=None, embed=embed)


    @unload.error
    async def unload_error(self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError) -> None:
        if isinstance(error, commands.NotOwner):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Can Only Be Used By The Bot's Owners.",
            )
            await ctx.respond(embed=embed)
        elif isinstance(error, ExtensionNotLoaded):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Extension Is Not Loaded.",
            )
            await ctx.respond(embed=embed)
        elif isinstance(error, ExtensionNotFound):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Extension Does Not Exist.",
            )
            await ctx.respond(embed=embed)
        else:
            traceback.print_exception(type(error), error, error.__traceback__)
            raise error


    @cogs.command(name="reload", description="Reload An Cog")
    @commands.is_owner()
    async def reload(self, ctx: discord.ApplicationContext, *, extension: str) -> None:
        if self.bot.development_mode != "development":
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `bot.development_mode` set to `{self.bot.development_mode}`, commands such as `load`, `reload` and `unload` require `bot.development_mode` to be **development**",
            )
            await ctx.respond(embed=embed)
        
        embed: Embed = discord.Embed(color=Colors.DEFAULT, description=f"{Emoji.LOADING_DOTS} Reloading Extension...")
        interaction = await ctx.respond(content=None, embed=embed)
        
        self.bot.unload_extension(f"cogs.{extension}.{extension}")
        self.bot.load_extension(f"cogs.{extension}.{extension}")
        
        embed: Embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.CHECKMARK} Successfully Reloaded `{extension}`",
        )
        await interaction.edit_original_response(content=None, embed=embed)


    @reload.error
    async def reload_error(self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError) -> None:
        if isinstance(error, commands.NotOwner):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Can Only Be Used By The Bot's Owners.",
            )
        elif isinstance(error, ExtensionNotLoaded):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Extension Is Not Loaded.",
            )
            await ctx.send(embed=embed)
        elif isinstance(error, ExtensionNotFound):
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} This Extension Does Not Exist.",
            )
            await ctx.send(embed=embed)
        else:
            traceback.print_exception(type(error), error, error.__traceback__)
        
def setup(bot):
    bot.add_cog(AFK(bot))