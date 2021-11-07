import discord
import traceback

from discord.ext import commands

from helpers.constants import *


class ErrorHandler(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot) -> None:
        self.bot = bot

    def convert(self, time):
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        return (int(day), int(hour), int(minutes), int(seconds))

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandOnCooldown):
            global time

            time = error.retry_after

            day, hour, minutes, seconds = self.convert(time)

            embed = discord.Embed(
                color=Colors.EMBED_COLOR,
                description=f"**The Command `{ctx.command}` Is On Cooldown!\n\n`{day}` Days, `{hour}` Hours, `{minutes}` Minutes and `{seconds}` Seconds Left.**",
            )
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.set_author(
                name=ctx.author.name, icon_url=ctx.author.avatar.url
            )
            embed.set_footer(
                text=f"ID: {ctx.author.id}", icon_url=ctx.author.avatar.url
            )

            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                color=Colors.ERROR_COLOR,
                description=f"{Emoji.ERROR} The command `{ctx.prefix}{ctx.command}` was not found!, If you would like this command to be added suggest it in our [support server]({Links.SUPPORT_SERVER_INVITE})",
            )
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.set_author(
                name=ctx.author.name,
                url=Links.BOT_DOCUMENTATION_URL,
                icon_url=ctx.author.avatar.url,
            )
            embed.set_footer(
                text=f"ID: {ctx.author.id}", icon_url=ctx.author.avatar.url
            )

        else:
            traceback.print_exception(type(error), error, error.__traceback__)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
