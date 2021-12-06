"""Boules Cog for the "BotAToutFer" discord bot

(C) 2021 Clément SEIJIDO
Released under GNU General Public License v3.0 (GNU GPLv3)
e-mail clement@seijido.fr
"""

import os
import json
import random

from discord.ext import commands
from discord.ext.commands import UserConverter


def setup(bot):
    bot.add_cog(Boules(bot))


class Boules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Path of the json file containing the balls counter
        self.BOULES_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "boules.json"
        )
        self.messages = [
            "J'aurais pas aimé...",
            "Sans rancune hein ?",
            "Ouch alors ça, qu'on soit de cet univers ou d'un autre, ça doit "
            "faire très très mal !",
            "Ah, ça a fait un sale bruit.",
            "À force, elles seront comme du fer.",
            "La prochaine fois je lui ferai pas confiance...",
            "Je peux même fournir le bâton :innocent:",
            "Je comprendrai jamais le goût qu'ont les humains pour le "
            "masochisme...",
            "Moi ça m'en touche une sans faire bouger l'autre",
            "C'est en voyant un moustique se poser sur ses testicules qu'on "
            "réalise qu'on ne peut pas régler tous les problèmes par la "
            "violence...",
            "Jingle Bells, Jingle Bells... :bell:",
            "Si j'en avais je compatirais",
            "Écouter la douleur c'est déjà l'adoucir",
        ]

    @commands.command(
        name="boules",
        help="Envie de vous tabasser les boules ?"
    )
    async def boules(self, ctx, *, user=None):
        try:  # Try to retrieve the balls history from file
            with open(self.BOULES_PATH, "r") as f:
                boules = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            # boules.json does not exist, we create a empty dictionary
            self.bot.log.error("boules.json file not found: ", exc_info=e)
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
            response = f"{ctx.author.mention} a envie de tabasser les " \
                       f"boules de {mention} "

        else:
            response = f"{ctx.author.mention} a envie de se tabasser les " \
                       f"boules "

        response += f"({channel_balls} paires de boules tabassées dans ce " \
                    f"salon, {boules['total']} au total).\n"
        response += random.choice(self.messages)

        await ctx.send(response)

    @commands.command(name="boule", hidden=True)
    async def boule(self, ctx):
        response = f"Ah, {ctx.author.mention} est monoboule ?"
        await ctx.send(response)
