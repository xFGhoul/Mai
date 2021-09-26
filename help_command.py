from typing import Mapping, Optional, List

from discord import Embed
from discord.ext import commands

from utils.constants import EMBED_COLOR, ERROR_EMOJI, ERROR_COLOR, CHECKMARK_EMOJI, QUESTION_EMOJI, BOT_AVATAR_URL, SUPPORT_SERVER_INVITE

class MaiHelpCommand(commands.HelpCommand):
    def command_not_found(self, string: str) -> str:
        return f"{ERROR_EMOJI} The command `{self.clean_prefix}{string}` was not found!, If you would like this command to be added suggest it in our [support server]({SUPPORT_SERVER_INVITE})"

    def subcommand_not_found(self, command: commands.Command, string: str) -> str:
        return f'{ERROR_EMOJI} I don\'t have the command `{command.qualified_name} {string}`, If you would like this command to be added suggest it in our [support server]({SUPPORT_SERVER_INVITE})'

    async def dispatch_help(self, help_embed: Embed) -> None:
        dest = self.get_destination()
        await dest.send(embed=help_embed)

    async def send_error_message(self, error: str) -> None:
        embed = Embed(
            title='Error :\\',
            description=f"{error}",
            color=ERROR_COLOR
        )
        await self.dispatch_help(embed)

    async def send_bot_help(
        self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]
    ) -> None:
        bot = self.context.bot
        embed = Embed(
            title=f"{bot.user.name} Help",
            description=f"**{CHECKMARK_EMOJI} Here is a full list of my commands!**",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=BOT_AVATAR_URL)
        for cog in self.context.bot.cogs.values():
            embed.add_field(name=cog.qualified_name, value=f'`{self.clean_prefix}help {cog.qualified_name}`', inline=True)
        await self.dispatch_help(embed)

    async def send_command_help(self, command: commands.Command) -> None:
        embed = Embed(
            title=f'Help For Command: `{command.name}`',
            color=EMBED_COLOR
        )
        embed.add_field(name=f'{QUESTION_EMOJI} What does this command do?', value=command.description, inline=False)
        embed.add_field(name='Usage', value=f'`{self.get_command_signature(command)}`', inline=False)
        await self.dispatch_help(embed)

    async def send_group_help(self, group: commands.Group) -> None:
        embed = Embed(
            title=f'Help For Command: `{group.name}`',
            color=EMBED_COLOR
        )
        embed.add_field(name=f'{QUESTION_EMOJI} What does this command do?', value=group.description, inline=False)
        embed.add_field(name='Usage', value=f'`{self.get_command_signature(group)}`', inline=False)
        subcommand_help = [f'**`{self.get_command_signature(command)}`**\n{command.description}' for command in group.commands]
        newline = '\n'
        embed.add_field(name='Related commands', value=f'\n{newline.join(subcommand_help)}', inline=False)
        await self.dispatch_help(embed)

    async def send_cog_help(self, cog: commands.Cog) -> None:
        embed = Embed(
            title=f'Help For Module: `{cog.qualified_name}`',
            color=EMBED_COLOR
        )
        embed.add_field(name=f'{QUESTION_EMOJI} What does this category do?', value=cog.description, inline=False)
        for command in cog.walk_commands():
            if command.parent is None:
                embed.add_field(
                    name=f'`{self.clean_prefix}{command.name}`', value=command.description)
        await self.dispatch_help(embed)
