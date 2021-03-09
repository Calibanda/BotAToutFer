# boules commands for BotÀToutFer
import os
import json
import random

import discord
from discord.ext import commands
from discord.ext.commands import UserConverter

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
            "Sans rancune hein ?",
            (
                "Ouch alors ça, qu'on soit de cet univers ou d'un autre,"
                + " ça doit faire très très mal !"
            ),
            "Ah, ça a fait un sale bruit."
        ]

    @commands.command(
        name="boules",
        help="Envie de vous tabasser les boules ?")
    async def boules(self, ctx, *, user=None):
        try:  # Try to retrieve the balls history from file
            with open(self.BOULES_PATH, "r") as f:
                boules = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            # boules.json does not exist, we create a empty dictionary
            self.bot.log.error(f"Catched exeption:", exc_info=e)
            boules = {
                'total': 0
            }

        if str(ctx.channel.id) in boules:
            boules[str(ctx.channel.id)] += 1
        else:
            boules[str(ctx.channel.id)] = 1

        boules["total"] += 1

        channel_balls = boules[str(ctx.channel.id)]

        with open(self.BOULES_PATH, "w") as f:
            # Save dictionary in boules.json
            json.dump(boules, f, indent=4)

        try:
            converter = UserConverter()
            user = await converter.convert(ctx, user)
            mention = user.mention
        except Exception as e:
            mention = user

        if user:
            response = (
                f"{ctx.author.mention} a envie de tabasser "
                + f"les boules de {mention} "
            )

        else:
            response = (
                f"{ctx.author.mention} a envie de se tabasser les boules "
            )

        response += (
            f"({channel_balls} paires de boules tabassées "
            + f"dans ce salon, {boules['total']} au total).\n"
            + random.choice(self.messages)
        )

        await ctx.send(response)
