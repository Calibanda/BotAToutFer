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
        self.bot.log.warning("Start birthday loop")
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

        for channel_id in birthdays:
            for user_id in birthdays[channel_id]:
                if birthdays[channel_id][user_id][:5] == today[:5]:
                    user = await self.bot.fetch_user(int(user_id))
                    if user is None:
                        self.bot.log.warning(
                            f"No user found with id {user_id}"
                        )
                        continue

                    channel = await self.bot.fetch_channel(channel_id)
                    if channel is None:
                        self.bot.log.warning(
                            f"No channel found with id {channel_id} to "
                            f"wish birthday to {user_id}"
                        )
                        continue

                    message = f"Bon anniversaire {user.mention} ! :tada:"
                    await channel.send(message)

    @birthday_loop.before_loop
    async def before_birthday_loop(self):
        await self.bot.wait_until_ready()

        self.bot.log.warning("Start before_birthday_loop")

        alarm = datetime.datetime.now().replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0
        )
        delta = (alarm - datetime.datetime.now()).total_seconds()
        if delta < 0:  # 9AM is passed today
            delta += datetime.timedelta(days=1).total_seconds()

        self.bot.log.warning(f"sleep {delta} seconds")
        await asyncio.sleep(delta)  # await next 9AM

    @birthday_loop.error
    async def error_birthday_loop(self, e):
        self.bot.log.error("Error during birthday loop", exc_info=e)
        self.birthday_loop.restart()

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

            try:
                date = birthdays[ctx.guild.id][ctx.user.id]
            except KeyError as e:
                response = f"Jamais entendu parler de cette personne"
            else:
                response = f"L'anniv de cette chouette personne est le {date}"
        else:
            response = f"Jamais entendu parler de cette personne"
        await ctx.send(response)

    @commands.command(
        name="mon-anniv",
        help="Permet d'enregistrer sa date de naissance"
    )
    async def mon_anniv(self, ctx, date: str = ""):
        try:
            date = parser.parse(date, dayfirst=True)
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

        if ctx.channel.id in birthdays:
            birthdays[ctx.channel.id][ctx.author.id] = f"{date.day:02d}/" \
                                                       f"{date.month:02d}/" \
                                                       f"{date.year}"
        else:
            birthdays[ctx.channel.id] = {
                ctx.author.id: f"{date.day:02d}/{date.month:02d}/{date.year}"
            }

        with open(self.BIRTHDAYS_PATH, "w") as f:
            json.dump(birthdays, f, indent=4)

        response = "C'est bon ! Je me souviendrai de ta date de naissance !"
        await ctx.send(response)
