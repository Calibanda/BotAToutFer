# boules commands for BotÀToutFer
import os
import json
import random

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Boules(bot))


class Boules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        # Path of the json file containing the balls counter
        self.BOULES_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "boules.json"
            )
        self.messages = [
            "J'aurais pas aimé...",
            "Sans racune hein ?",
            (
                "Ouch alors ça, qu'on soit de cet univers ou d'un autre,"
                + " ça doit faire très très mal !"
            ),
            "Ah, ça a fait un sale bruit."
        ]

    @commands.command(
        name="boules",
        help="Envie de vous tabasser les boules ?")
    async def boules(self, ctx, user: discord.User = None):
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

        try:
            mention = user.mention
        except Exception
            mention = user

        if user:
            response = (
                f"{ctx.author.mention} a envie de tabasser les boules de"
                + f"{mention} ({channel_balls} paires de boules "
                + f"tabassées dans ce salon, {boules['total']} au total).\n"
                + random.choice(self.messages)
            )

        else:
            response = (
                f"{ctx.author.mention} a envie de se tabasser les boules "
                + f"({channel_balls} paires de boules "
                + f"tabassées dans ce salon, {boules['total']} au total)."
            )

        await ctx.send(response)
