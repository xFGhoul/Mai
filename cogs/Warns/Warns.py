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
import uuid

from typing import Optional, Union, Tuple, TYPE_CHECKING

from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.ext.commands import Bot, BucketType

from utils.console import console
from utils.custom import MaiCog
from utils.constants import Colors, Emoji, Links, MAI, Limitations

from PycordUtils.Pagination import AutoEmbedPaginator

if TYPE_CHECKING:
    from mai import Mai

class Warns(
    MaiCog,
    name="Warns",
    description="warn",
    emoji=Emoji.DISCORD_OFFICIAL_MODERATOR,
):
    def __init__(self, bot: commands.Bot):
        self.bot: Mai = bot
        
    warns = SlashCommandGroup(name="warns", description="Warn Bad Actors", guild_ids=[MAI.SUPPORT_SERVER_ID])
        
    @warns.command(name="warn", description="Warn Members")
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx: discord.ApplicationContext, member: discord.Member, *, reason: str) -> None:
        if member == ctx.author:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} Cannot Warn Yourself.",
            )
            await ctx.respond(embed=embed, delete_after=15)
            return
        
        if len(reason) > Limitations.MAX_WARNING_REASON:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} Reason Must Be Below `350` Characters.",
            )
            await ctx.respond(embed=embed, delete_after=15)
            return
        
        warn_id: str = str(uuid.uuid4())
        
        warns = await self.bot.db.execute("INSERT INTO warns(warn_id, guild_id, warned_id, warner_id, reason) VALUES($1, $2, $3, $4, $5)", warn_id, ctx.guild.id, member.id, ctx.author.id, reason)
        await ctx.respond(warns)
        
        
    @warns.command(name="clear", description="Clear A Certain Warning or All Warnings")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: discord.ApplicationContext, clear: str) -> None:
        ...
        
    @warns.command(name="list", description="Shows A List Of A Users Total Warns")
    @commands.has_permissions(manage_messages=True)
    async def list(self, ctx: discord.ApplicationContext, member: discord.Member) -> None:
        ...
        
        
def setup(bot):
    bot.add_cog(Warns(bot))