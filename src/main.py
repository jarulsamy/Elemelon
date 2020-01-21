# -*- coding: utf-8 -*-
import asyncio
import os
import random

import discord
import globals
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
from MelonGame import clean_row
from MelonGame import Melon

load_dotenv()

BOT_PREFIX = "?"
TOKEN = os.getenv("TOKEN")


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kill(self, ctx):
        await ctx.send(f"Stopping upon the request of {ctx.author.mention}")
        await self.bot.close()
        exit(0)

    @commands.command()
    async def stop(self, ctx):
        await ctx.send(f"Stopping upon the request of {ctx.author.mention}")
        await self.bot.close()
        exit(0)


class Beezus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = None
        self.player = None
        self.prepped = False

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"Hello {member}")

    @commands.command()
    async def new_game(self, ctx):
        await ctx.send(f"Creating a new game with {ctx.author.mention}")

        self.player = ctx.author
        self.game = Melon()
        for row in self.game.board:
            await ctx.send(clean_row(row))

        await ctx.send(
            "Select your passive, basic, crowd control, and self-boot abilities."
        )
        await ctx.send(f"Use {BOT_PREFIX}set_abilities PASSIVE BASIC CC SB")

    @commands.command()
    async def set_abilities(self, ctx, *args):
        if self.game is None:
            await ctx.send("No game in progress?")
            return
        elif ctx.author != self.player:
            return

        args = [i.lower() for i in args]
        if len(args) != len(globals.Abilities):
            await ctx.send("Incorrect number of abilities!\nTry Again!")
            return
        try:
            self.game.Player.player_abilities = args
        except ValueError:
            await ctx.send("One of your selections is invalid!\nTry Again!")
            return
        else:
            await ctx.send(f"Abilities set: {self.game.Player.player_abilities}")
            self.prepped = True
            await ctx.send(f"Start the game with {BOT_PREFIX}start_game")

    @commands.command()
    async def start_game(self, ctx):
        if self.game is None:
            await ctx.send("No game in progress?")
            return
        elif ctx.author != self.player:
            return

        # TODO: add this back in, off for debugging
        # if not self.prepped:
        #     await ctx.send("Game not ready yet!")
        #     return

        await ctx.send("Randomly selecting who goes first...")
        starting_player = random.randint(0, 1)
        if starting_player == 1:
            await ctx.send(f"{self.player.mention}, you go first, darn :X")
        else:
            await ctx.send(f"Haha I go first, totally not a biased coin flip")
        return

    def _reset_game(self):
        self.game = None
        self.player = None
        self.prepped = False

    @commands.command()
    async def stop_game(self, ctx):
        if self.game is None:
            await ctx.send("No game in progress?")
            return
        elif ctx.author != self.player:
            return
        self._reset_game()
        await ctx.send(f"Game cancelled!")


if __name__ == "__main__":
    # client.run(TOKEN)
    bot = Bot(command_prefix=BOT_PREFIX)
    bot.add_cog(GeneralCommands(bot))
    bot.add_cog(Beezus(bot))
    bot.run(TOKEN)
