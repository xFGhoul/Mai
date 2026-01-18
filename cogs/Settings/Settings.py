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

from typing import TYPE_CHECKING

from discord.commands import SlashCommandGroup
from discord.ext import commands

from utils.custom import MaiCog
from utils.constants import Colors, Emoji

if TYPE_CHECKING:
    from mai import Mai


class Settings(MaiCog, emoji=Emoji.DISCORD_OFFICIAL_MODERATOR):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: Mai = bot
        
    settings = SlashCommandGroup("settings", "Manage Guild Settings")
    
    prefix = settings.create_subgroup("prefix", "Manage Guild Prefix", guild_only=True)
    
    @settings.command(name="hello", description="Say Hello :)")
    async def hello(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond("Hello.")
    
    @prefix.command(name="view", description="View The Current Guild Prefix")
    async def prefix_view(self, ctx: discord.ApplicationContext) -> None:
        prefix = await self.bot.db.fetchval("SELECT prefix FROM guild where discord_id = $1", ctx.guild.id)
        embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{ctx.author.mention}, My current prefix is `{prefix}` or {self.bot.user.mention}",
            )
        await ctx.respond(embed=embed)
        
    @prefix.command(name="set", description="Set The Guild's Prefix")
    @discord.default_permissions(administrator=True)
    async def prefix_set(self, ctx: discord.ApplicationContext, prefix: str) -> None:
        await self.bot.db.execute("UPDATE guild SET prefix = $1 WHERE discord_id = $2", prefix, ctx.guild.id)
        embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"I set your guild's prefix to `{prefix}`",
            )
        await ctx.respond(embed=embed)
        
    @prefix.command(name="reset", description="Reset Guild Prefix")
    @discord.default_permissions(administrator=True)
    async def prefix_reset(self, ctx: discord.ApplicationContext) -> None:
        await self.bot.db.execute("UPDATE guild SET prefix = $1 WHERE discord_id = $2", self.bot.default_prefix, ctx.guild.id)
        embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Emoji.CHECKMARK} Successfully reseted {ctx.guild.name} ({ctx.guild.id}) prefix to `{self.bot.default_prefix}`",
            )
        await ctx.respond(embed=embed)
        
        
def setup(bot):
    bot.add_cog(Settings(bot))