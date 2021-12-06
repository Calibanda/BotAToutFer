"""Anniversaire Cog for the "BotAToutFer" discord bot

(C) 2021 Clément SEIJIDO
Released under GNU General Public License v3.0 (GNU GPLv3)
e-mail clement@seijido.fr
"""

import os
import datetime
import json
import asyncio

import discord
from discord.ext import commands, tasks
import dateutil.parser as parser


def setup(bot):
    bot.add_cog(Anniversaire(bot))


class Anniversaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Path of the json file containing the users birthdays
        self.BIRTHDAYS_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "birthdays.json"
        )

        self.birthday_loop.start()

    def cog_unload(self):
        self.birthday_loop.cancel()

    @tasks.loop(hours=24)
    async def birthday_loop(self):
        try:
            with open(self.BIRTHDAYS_PATH, "r") as f:
                birthdays = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error(
                "birthdays.json file not found: ",
                exc_info=e
            )
            birthdays = {}

        now = datetime.datetime.now()
        today = f"{now.day:02d}/{now.month:02d}"  # DD/MM

        for user in birthdays:
            if birthdays[user]["birthdate"][:5] == today:
                message = f"Bon anniversaire " \
                          f"{self.bot.get_user(user).mention} ! :tada:"
                server = self.bot.get_guild(birthdays[user]["server_id"])
                await server.system_channel.send(message)

    @birthday_loop.before_loop
    async def before_birthday_loop(self):
        await self.bot.wait_until_ready()

        alarm = datetime.datetime.now().replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0
        )
        delta = (alarm - datetime.datetime.now()).total_seconds()
        if delta < 0:  # 9AM is passed today
            delta += datetime.timedelta(days=1).total_seconds()

        await asyncio.sleep(delta)  # await next 9AM

    @commands.command(
        name="anniv",
        help="Affiche l'anniversaire d'un utilisateur humain"
    )
    async def anniv(self, ctx, user: discord.User):
        if user:
            try:
                with open(self.BIRTHDAYS_PATH, "r") as f:
                    birthdays = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
                self.bot.log.error(
                    "birthdays.json file not found: ",
                    exc_info=e
                )
                birthdays = {}

            if str(user.id) in birthdays:
                date = birthdays[str(user.id)]["birthdate"][:5]  # DD/MM
                response = f"L'anniv de cette chouette personne est le {date}"
            else:
                response = f"Jamais entendu parler de cette personne"
        else:
            response = f"Jamais entendu parler de cette personne"
        await ctx.send(response)

    @commands.command(
        name="mon-anniv",
        help="Permet d'enregistrer sa date de naissance"
    )
    async def mon_anniv(self, ctx, date: str = ""):
        try:
            date = parser.parse(date)
        except parser.ParserError as e:
            response = "Euhhh, c'est quoi cette date bourrée ?"
            await ctx.send(response)
            return

        try:
            with open(self.BIRTHDAYS_PATH, "r") as f:
                birthdays = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error(
                "birthdays.json file not found: ",
                exc_info=e
            )
            birthdays = {}

        birthdays[str(ctx.author.id)] = {
            "server_id": str(ctx.guild.id),
            "birthdate": f"{date.day:02d}/{date.month:02d}/{date.year}"
        }

        with open(self.BIRTHDAYS_PATH, "w") as f:
            json.dump(birthdays, f, indent=4)

        response = "C'est bon ! Je me souviendrai de ta date de naissance !"
        await ctx.send(response)
