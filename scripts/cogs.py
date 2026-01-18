import click
import os

from rich.console import Console
from pathlib import Path

FOOTER = """

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""
ROOT_DIR = Path(__file__).absolute().parent.parent
COGS_DIR = os.path.join(ROOT_DIR, "cogs")

console = Console()

@click.group(name="cog")
def cog() -> None:
    pass

@cog.command(name="create")
@click.option("--cog_name", default="Test",  help="Name of the new cog")
@click.option("--cog_desc", default="Test", help="Description of the new cog")
@click.option("--cmd_name", default="test", help="Name of the example command")
@click.option("--cmd_desc", default="Example cmd",help="Description of the example command")
def create(cog_name, cog_desc, cmd_name, cmd_desc) -> None:
    console.print(f"[blue3] [MAI] Creating [green]{cog_name}[/green] and [green]{cmd_name}[/green]")
    maiCog = f'"""{FOOTER}"""' + f"""
    
import discord

from typing import Optional, TYPE_CHECKING

from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from utils.console import console
from utils.custom import MaiCog
from utils.constants import Colors, Emoji, Links, MAI

if TYPE_CHECKING:
    from mai import Mai

class {cog_name}(
    MaiCog,
    name="{cog_name}",
    description="{cog_desc}",
    emoji=Emoji.MAI,
):
    def __init__(self, bot: commands.Bot):
        self.bot: Mai = bot
        
    @commands.slash_command(name="{cmd_name}", description="{cmd_desc}")
    @commands.cooldown(1, 1, BucketType.user)
    async def {cmd_name}(self, ctx: discord.ApplicationContext) -> None:
        ...
    
def setup(bot):
    bot.add_cog({cog_name}(bot))"""
    
    cog_path = os.path.join(COGS_DIR, cog_name)
    os.mkdir(cog_path)
    
    with open(os.path.join(cog_path, f"{cog_name}.py"), mode="+w", encoding="UTF-8") as file:
        file.write(maiCog)
    console.print(f"[blue3] [MAI] Created [green]{cog_name}[/green] and [green]{cmd_name}[/green]")
    
    
cog.add_command(create)
    
if __name__ == "__main__":
    cog()