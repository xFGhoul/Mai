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
import pickle
import random
import aiofiles


from discord.ext import commands
from discord.ext.commands import BucketType

from helpers.constants import *
from helpers.logging import log
from helpers.cache.reddit import RedditPostCacher


class NSFW(
    commands.Cog,
    name="NSFW",
    description="NSFW(Not Safe For Work) Commands :smirk:",
):
    def __init__(self, bot):
        self.bot = bot
        self.subreddits = (
            "ass",
            "LegalTeens",
            "boobs",
            "pussy",
            "TooCuteForPorn",
            "Nudes",
            "cumsluts",
            "hentai",
        )
        self.cache = RedditPostCacher(
            self.subreddits, "./cogs/NSFW/cache/NSFW.pickle"
        )
        self.cache.cache_posts.start()

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    async def _reddit_sender(
        self, ctx: commands.Context, subrd: str, title: str
    ):
        """Fetches from reddit and sends results
        Parameters
        ----------
        ctx : discord.ext.commands.Context
                The invocation context
        subrd : str
                The subreddit to fetch from
        title : str
                The title to use in the embed
        """
        submission = await self.cache.get_random_post(subrd)

        embed = discord.Embed(
            title=title,
            timestamp=ctx.message.created_at,
            colour=discord.Color.dark_purple(),
        )
        embed.set_image(url=submission)
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = discord.Embed(
                title="NSFW not allowed here",
                description="Use NSFW commands in a NSFW marked channel.",
                color=Colors.ERROR_COLOR,
            )
            embed.set_image(url=Links.NSFW_CHANNEL_REQUIRED)
            await ctx.send(embed=embed)
        else:
            traceback.print_exception(type(error), error, error.__traceback__)

    @commands.command(name="ass", description="Ass Pictures", brief="ass")
    @commands.guild_only()
    @commands.is_nsfw()
    async def ass(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "ass", "DRUMS")

    @commands.command(name="teen", description="Legal Teenagers", brief="teen")
    @commands.guild_only()
    @commands.is_nsfw()
    async def teen(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "LegalTeens", "You like them young?")

    @commands.command(name="boobs", description="Boob Pictures", brief="boobs")
    @commands.guild_only()
    @commands.is_nsfw()
    async def boobs(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "boobs", "Bounce! Bounce!")

    @commands.command(name="pussy", description="Pussy Pictures", brief="pussy")
    @commands.guild_only()
    @commands.is_nsfw()
    async def pussy(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "pussy", "Wet or Dry?")

    @commands.command(
        name="cutesluts", description="Cute Pictures", brief="cutesluts"
    )
    @commands.guild_only()
    @commands.is_nsfw()
    async def cutesluts(self, ctx: commands.Context) -> None:
        await self._reddit_sender(
            ctx, "TooCuteForPorn", "Too cute for porn, aren't they?"
        )

    @commands.command(name="nudes", description="nude pictures", brief="nudes")
    @commands.guild_only()
    @commands.is_nsfw()
    async def nudes(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "Nudes", "Sick of pornstars? Me too!")

    @commands.command(
        name="cum",
        aliases=["cumsluts"],
        description="Cumslut Pictures",
        brief="cum",
    )
    @commands.guild_only()
    @commands.is_nsfw()
    async def cum(self, ctx: commands.Context) -> None:
        await self._reddit_sender(
            ctx, "cumsluts", "And they don't stop cumming!"
        )

    @commands.command(
        name="hentai", description="Hentai Pictures", brief="hentai"
    )
    @commands.guild_only()
    @commands.is_nsfw()
    async def hentai(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "hentai", "AnImE iS jUsT CaRtOoN")


def setup(bot):
    bot.add_cog(NSFW(bot))
