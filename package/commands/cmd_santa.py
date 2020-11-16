# hanged commands for BotAToutFer
import os
import random

import discord
from discord.ext import commands

import const

class Santa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name="santa", help="Tire les pèrers Noëls secret avec les utilisateurs précisés")
    async def santa(self, ctx, *users: discord.User):
        if len(users) < 2:
            response = "Il faut au moins 2 personnes pour tirer les pères Noël secrets !"
            ctx.send(response)
            return

        christmas_is_ready = False

        while not christmas_is_ready:
            senders = list(users)
            recipients = list(users)
            list_couples = []

            for sender in senders:
                recipient = random.choice(recipients)
                recipients.remove(recipient)

                list_couples.append((sender, recipient))
            
            christmas_is_ready = True

            for couple in list_couples:
                if couple[0] == couple[1]:
                    christmas_is_ready = False

        for sender, recipient in list_couples:
            dm_channel = sender.dm_channel if sender.dm_channel else await sender.create_dm()
            message = f"Salut {sender.name} ! Le tirage au sort des Pères Noëls secrets à été effectué :santa: \nIl ne te reste plus qu'à trouver un cadeau pour <@{recipient.id}> :gift_heart:. Et un joyeux Noël à tous ! "
            await dm_channel.send(message)
