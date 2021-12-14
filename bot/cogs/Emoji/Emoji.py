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
import re


from discord import (
    PartialEmoji,
    Embed,
    Color,
    Message,
    PartialEmoji,
    HTTPException,
)

from typing import Set

from discord.ext import commands
from discord.ext.commands import Greedy, BucketType

from helpers.constants import *
from helpers.logging import log

from asyncio import Event


class Emoji(commands.Cog, name="Emoji", description="Helpful Emoji Utilities"):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_extraction_pattern = re.compile(
            r"<(a?):([a-zA-Z0-9\_]+):([0-9]+)>"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(name="emoji", aliases=["emote"])
    async def emoji(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await self.bot.send_help(ctx.command)

    async def extract_emoji_from_messages(
        self, messages: discord.Message
    ) -> Set:
        parsed_emoji = set()
        for message in messages:
            for match in self.emoji_extraction_pattern.finditer(
                message.content
            ):
                animated = bool(match.group(1))
                name = match.group(2)
                emoji_id = int(match.group(3))
                emoji = PartialEmoji.with_state(
                    self.bot._connection,
                    animated=animated,
                    name=name,
                    id=emoji_id,
                )
                parsed_emoji.add(emoji)
        return parsed_emoji

    async def copy_emoji_to_guild(
        self, emoji: discord.Emoji, guild: discord.Guild
    ) -> discord.Emoji:
        created_emoji = await guild.create_custom_emoji(
            name=emoji.name, image=await emoji.read()
        )
        return created_emoji

    def message_contains_emoji(self, message: discord.Message):
        match = self.emoji_extraction_pattern.search(message.content)
        return match is not None

    @commands.has_guild_permissions(manage_emojis=True)
    @emoji.command(
        name="add",
        description="Add Multiple Emojis To A Server",
        brief="add :emoji1: :emoji2: :emoji3:",
    )
    async def add_emoji(
        self,
        ctx: commands.Context,
        emojis: Greedy[PartialEmoji],
        messages: Greedy[Message],
    ) -> None:

        if not emojis and not messages:
            last_message = [
                await ctx.history(limit=10).find(
                    lambda m: self.message_contains_emoji(m)
                )
            ]
            if None in last_message:
                last_message = []
            emojis = await self.extract_emoji_from_messages(last_message)
        elif messages:
            emojis = await self.extract_emoji_from_messages(messages)
        added_emoji = set()
        async with ctx.channel.typing():
            limit_reached = Event()
            for emoji in filter(lambda e: e.is_custom_emoji(), emojis):
                try:
                    created_emoji = await self.copy_emoji_to_guild(
                        emoji, ctx.guild
                    )
                    added_emoji.add(created_emoji)
                except HTTPException:
                    limit_reached.set()
                    break
        if added_emoji:
            summary = Embed(
                title="New emoji added ✅",
                description="\n".join(
                    f"\\:{emoji.name}\\: -> {emoji}" for emoji in added_emoji
                ),
                color=Color.green(),
            )
            if limit_reached.is_set():
                summary.description += (
                    "\nSome emoji were not added because you hit the limit."
                )
        elif not added_emoji and limit_reached.is_set():
            summary = Embed(
                title="Emoji limit reached ⛔",
                description="You have reached the max emoji for this server, get more boosts to raise this limit!",
                color=Color.red(),
            )
        else:
            messages_given = bool(messages)
            error_message = (
                "message(s) given" if messages_given else "last 10 messages"
            )
            summary = Embed(
                title="No emoji found 😔",
                description=f"No emoji were found in the {error_message}",
                color=0xFFFF00,
            )
        await ctx.send(embed=summary)


def setup(bot):
    bot.add_cog(Emoji(bot))
