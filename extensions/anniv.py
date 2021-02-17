# anniv commands for BotÀToutFer
import os
import datetime
import json
import re

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Anniversaire(bot))


class Anniversaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.BIRTHDAYS_PATH = os.path.join(self.bot.SCRIPT_DIR, "package", "birthdays.json") # The path of the json file containing the users birthdays

    @commands.command(name="anniv", help="Affiche l'anniversaire d'un utilisateur humain")
    async def anniv(self, ctx, user:discord.User):
        if user:
            try:
                with open(self.BIRTHDAYS_PATH, "r") as f:
                    birthdays = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
                self.bot.log.error(f"Catched exeption:", exc_info=e)
                birthdays = {}

            if str(user.id) in birthdays:
                response = f"L'anniv de cette chouette personne est le {birthdays[str(user.id)][:-5]}"
            else:
                response = f"Jamais entendu parler de cette personne"
        else:
            response = f"Jamais entendu parler de cette personne"
        await ctx.send(response)


    @commands.command(name="mon_anniv", help="Permet d'enregistrer sa date de naissance sous la forme DD/MM/YYYY")
    async def mon_anniv(self, ctx, date:str=""):
        date = re.search(r"\d{2}\/\d{2}\/\d{4}", date)[0]
        if date:
            try:
                with open(self.BIRTHDAYS_PATH, "r") as f:
                    birthdays = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
                self.bot.log.error(f"Catched exeption:", exc_info=e)
                birthdays = {}

            birthdays[ctx.author.id] = date

            with open(self.BIRTHDAYS_PATH, "w") as f:
                json.dump(birthdays, f, indent=4)

            response = f"C'est bon ! Je me souvendrai de ta date de naissance !"
        else:
            response = f"Euhhh, c'est quoi cette date bourrée ?"
        await ctx.send(response)
