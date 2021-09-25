from typing import Mapping, Optional, List

from discord import Embed, Color
from discord.ext import commands


class MaiHelpCommand(commands.HelpCommand):
    def command_not_found(self, string: str) -> str:
        pass

    def subcommand_not_found(self, command: commands.Command, string: str) -> str:
        pass

    async def dispatch_help(self, help_embed: Embed) -> None:
        pass

    async def send_error_message(self, error: str) -> None:
        pass

    async def send_bot_help(
        self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]
    ) -> None:
        pass

    async def send_command_help(self, command: commands.Command) -> None:
        pass

    async def send_group_help(self, group: commands.Group) -> None:
        pass

    async def send_cog_help(self, cog: commands.Cog) -> None:
        pass
