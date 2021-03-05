# boules commands for BotÀToutFer
import os
import json

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Boules(bot))


class Boules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.hidden_cog = True
        # Path of the json file containing the balls counter
        self.BOULES_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "boules.json"
            )

    @commands.command()
    async def boules(self, ctx):
        try:
            with open(self.BOULES_PATH, "r") as f:
                boules = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error(f"Catched exeption:", exc_info=e)
            boules = {}

        try:
            boules["total"] += 1
        except KeyError:
            boules["total"] = 1

        if str(ctx.channel.id) in boules:
            boules[str(ctx.channel.id)] += 1
        else:
            boules[str(ctx.channel.id)] = 1

        with open(self.BOULES_PATH, "w") as f:
            json.dump(boules, f, indent=4)

        channel_balls = boules[str(ctx.channel.id)]

        response = f"{ctx.author.mention} a envie de se tabasser les boules "
        response += f"({channel_balls} paires de boules tabassées dans ce salon, "
        response += f"{boules['total']} au total)."
        await ctx.send(response)