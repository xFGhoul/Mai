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

from typing import Optional, TYPE_CHECKING

from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from utils.console import console
from utils.custom import MaiCog
from utils.constants import Colors, Emoji, Links, MAI

if TYPE_CHECKING:
    from mai import Mai

class Music(
    MaiCog,
    name="Music",
    description="Music",
    emoji=Emoji.MAI,
):
    def __init__(self, bot: commands.Bot):
        self.bot: Mai = bot
        
    @commands.slash_command(name="spotify", description="Show Currently Playing Spotify Music")
    @commands.cooldown(1, 1, BucketType.user)
    async def spotify(self, ctx: discord.ApplicationContext, member: discord.Member) -> None:
        if member is None:
            member: discord.Member | None = ctx.author

        async with ctx.channel.typing():
            spotify = discord.utils.find(lambda a: isinstance(a, discord.Spotify), member.activities)
            
            if spotify is None:
                embed = discord.Embed(
                    color=Colors.ERROR,
                    description=f"{Emoji.ERROR} **{member}** is not listening or connected to Spotify.",
                )
                return await ctx.respond(embed=embed)

            image = await self.bot.jeyy_api.spotify_from_object(spotify)

            await ctx.send(
                f"> **{member}** is listening to **{spotify.title}**",
                file=discord.File(image, f"{member.name}-spotify.png"),
            )           
            
def setup(bot):
    bot.add_cog(Music(bot))