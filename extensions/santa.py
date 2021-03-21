# Santa secrets commands for BotÀToutFer
import os
import random

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Santa(bot))


class Santa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.hidden_cog = True

    @commands.command(name="santa", help="Tire les pères Noëls secret avec les utilisateurs précisés")
    @commands.has_role("Santa")
    async def santa(self, ctx, *users: discord.User):
        if len(users) < 2:
            response = "Il faut au moins 2 personnes pour tirer les pères Noël secrets !"
            await ctx.send(response)
            return

        senders = list(users)
        random.shuffle(senders)
        recipients = senders.copy()
        recipients.append(recipients[0])
        del recipients[0]

        for sender, recipient in zip(senders, recipients):
            if sender.dm_channel:
                dm_channel = sender.dm_channel
            else:
                dm_channel = await sender.create_dm()
            message = f"Salut {sender.name} ! Le tirage au sort des Pères Noëls secrets à été effectué :santa: \n"
            message += f"Il ne te reste plus qu'à trouver un cadeau pour {recipient} :gift_heart:. Et un joyeux Noël à tous !"
            await dm_channel.send(message)
