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
import os
import random
import json

from typing import Optional

from discord.ext import commands
from discord.ext.commands import Greedy

from helpers.constants import *
from helpers.logging import log

from config.ext.parser import ROOT_DIR


class Actions(commands.Cog, name="Actions", description="Fun Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.json_path = "assets/actions.json"

        with open(os.path.join(ROOT_DIR, self.json_path), "r") as json_file:
            self.links = json.load(json_file)

        self.hugs = self.links["hugs"]
        self.slaps = self.links["slaps"]
        self.kills = self.links["kills"]
        self.pats = self.links["pats"]
        self.licks = self.links["licks"]

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="poptart",
        description="Throws A Poptart At Random Members",
        brief="poptart @Member1 @Member2",
    )
    @commands.guild_only()
    async def poptart(
        self, ctx: commands.Context, target: Greedy[discord.Member]
    ) -> None:

        number_of_targets = len(target)
        speed_of_light = 299792458
        rand_percentage = random.random()
        percentage_of_speed = speed_of_light * rand_percentage
        if number_of_targets == 1:
            formatted_targets = target[0].mention
        elif number_of_targets == 2:
            formatted_targets = f"{target[0].mention} and {target[1].mention}"
        else:
            comma_separated = ", ".join(map(lambda m: m.mention, target[:-1]))
            final_element = f", and {target[-1].mention}"
            formatted_targets = f"{comma_separated}{final_element}"
        await ctx.send(
            f"{ctx.author.display_name} throws a poptart at {formatted_targets} with a mind numbing speed of "
            f"{int(percentage_of_speed)} m/s, that's {rand_percentage * 100:.2f}% the speed of light!"
        )

    @commands.command(
        name="hug", description="Hug Someone Or Yourself", brief="hug @Member1"
    )
    @commands.guild_only()
    async def hug(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} got hugged!",
                color=Colors.SUCCESS_COLOR,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} hugged {member.mention}",
                color=Colors.SUCCESS_COLOR,
            )
        random_link = random.choice(self.hugs)
        embed.set_image(url=random_link)
        await ctx.send(embed=embed)

    @commands.command(
        name="pat", description="Pat Someone Or Yourself", brief="pat @Member1"
    )
    @commands.guild_only()
    async def pat(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} got patted!",
                color=Colors.SUCCESS_COLOR,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} pats {member.mention}",
                color=Colors.SUCCESS_COLOR,
            )
        random_link = random.choice(self.pats)
        embed.set_image(url=random_link)
        await ctx.send(embed=embed)

    @commands.command(
        name="kill",
        description="Kill Someone Or Yourself",
        brief="kill @Member1",
    )
    @commands.guild_only()
    async def kill(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} is a murdurer!",
                color=Colors.SUCCESS_COLOR,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} KILLED {member.mention}",
                color=Colors.SUCCESS_COLOR,
            )
        random_link = random.choice(self.kills)
        embed.set_image(url=random_link)
        await ctx.send(embed=embed)

    @commands.command(
        name="slap",
        description="Slap Someone Or Yourself",
        brief="slap @Member1",
    )
    @commands.guild_only()
    async def slap(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} slapped!",
                color=Colors.SUCCESS_COLOR,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} slapped {member.mention}",
                color=Colors.SUCCESS_COLOR,
            )
        random_link = random.choice(self.slaps)
        embed.set_image(url=random_link)
        await ctx.send(embed=embed)

    @commands.command(
        name="lick",
        description="Lick Someone Or Yourself",
        brief="lick @Member1",
    )
    @commands.guild_only()
    async def lick(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} got licked.",
                color=Colors.SUCCESS_COLOR,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} licked {member.mention}",
                color=Colors.SUCCESS_COLOR,
            )
        random_link = random.choice(self.licks)
        embed.set_image(url=random_link)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Actions(bot))
