# quiz commands for BotAToutFer
import os
import random
import json
import re
import aiohttp
import datetime

import asyncio
import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Quiz(bot))


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.games = {}
        # games = {discord.Guild.id: {
        #     "langue": "",
        #     "categorie": "",
        #     "theme": "",
        #     "difficulte": "",
        #     "question": "",
        #     "reponse_correcte": "",
        #     "autres_choix": []
        #     "anecdote": "",
        #     "wikipedia": ""
        #     "starting_time": datetime.datetime
        #     "indice": False
        # }}

        self.API_URL = "https://www.openquizzdb.org/api.php"
        self.API_PARAMETERS = {
            "key": self.bot.OPENQUIZZDB_TOKEN,
            "lang": "fr",
            "mono": "0",
            "anec": "1",
            "wiki": "1"
        }
        self.api_last_call = None

    @commands.command(name="quiz", help="Demande une question du quiz")
    async def quiz(self, ctx, option=""):
        option = option.casefold().strip()

        if option == "":
            if ctx.guild.id in self.games:
                await self.send_question(ctx)
            else:
                await self.launch_game(ctx)

        elif option == "indice":
            if ctx.guild.id in self.games:
                await self.indice(ctx)
            else:
                await ctx.send("Il n'y a pas de quiz en cours dans ce serveur !")

        elif option == "stop":
            if ctx.guild.id in self.games:
                await self.stop(ctx)
            else:
                await ctx.send("Il n'y a pas de quiz en cours dans ce serveur !")

    @commands.Cog.listener('on_message')
    async def process_game(self, message):
        if message.guild.id in self.games:
            if self.games[message.guild.id]["reponse_correcte"].casefold().strip() in message.content:
                await self.win(message)

    async def launch_game(self, ctx):
        if self.api_last_call:
            delta = (datetime.datetime.now() - self.api_last_call).seconds
            if delta < 60:
                response = f"J'envoie une question dans {delta} seconde(s) !"
                await ctx.send(response)
                await asyncio.sleep(delta)

        async with aiohttp.ClientSession() as session:
            self.bot.log.warning(f"Asking for a quiz question")
            async with session.get(self.API_URL, params=self.API_PARAMETERS) as r:
                if r.status == 200:
                    self.api_last_call = datetime.datetime.now()
                    question = await r.json()
                    if question["response_code"] == 0:  # Succès
                        self.games[ctx.guild.id] = question["results"][0]
                        self.games[ctx.guild.id]["starting_time"] = datetime.datetime.now()
                        random.shuffle(self.games[ctx.guild.id]["autres_choix"])
                        self.games[ctx.guild.id]["indice"] = False
                        await self.send_question(ctx)
                    else:
                        self.bot.log.error(f"Problem with the API key, code: {question['response_code']}")
                        response = "Désolé, je n'ai pas réussi à trouver une question de quiz..."
                        await ctx.send(response)

    async def send_question(self, ctx):
        title = "Quiz - Catégorie " + self.games[ctx.guild.id]["categorie"] + " - Difficulté " + self.games[ctx.guild.id]["difficulte"]
        colors = {
            "débutant": 0x00ff00,
            "confirmé": 0xffcc00,
            "expert": 0xff0000
        }
        description = self.games[ctx.guild.id]["question"]
        embed = discord.Embed(
            title=title,
            description=description,
            color=colors[self.games[ctx.guild.id]["difficulte"]]
        )
        if self.games[ctx.guild.id]["indice"]:
            for autre_choix in self.games[ctx.guild.id]["autres_choix"]:
                embed.add_field(
                    name="Proposition",
                    value=autre_choix,
                    inline=True
                )
        await ctx.send(embed=embed)

    async def indice(self, ctx):
        self.games[ctx.guild.id]["indice"] = True
        await self.send_question(ctx)

    async def stop(self, ctx):
        title = "Quiz - Fin de la question"
        description = self.games[ctx.guild.id]["reponse_correcte"]
        embed = discord.Embed(title=title, description=description)
        embed.add_field(
            name="Anecdote",
            value=self.games[ctx.guild.id]["anecdote"],
            inline=True
        )
        embed.add_field(
            name="Un peu de culture",
            value=self.games[ctx.guild.id]["wikipedia"],
            inline=True
        )
        await ctx.send(embed=embed)
        del self.games[ctx.channel.id]

    async def win(self, message):
        title = "Quiz - Fin de la question"
        points = 0
        if self.games[message.guild.id]["difficulte"] == "débutant":
            points = 2
        elif self.games[message.guild.id]["difficulte"] == "confirmé":
            points = 4
        elif self.games[message.guild.id]["difficulte"] == "expert":
            points = 6

        if self.games[message.guild.id]["indice"]:
            points = int(points/2)

        description = f"Bravo {message.author.name}. La réponse était " + self.games[message.guild.id]["reponse_correcte"] + f". {points} point(s) !"
        embed = discord.Embed(title=title, description=description)
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        embed.add_field(
            name="Anecdote",
            value=self.games[message.guild.id]["anecdote"],
            inline=True
        )
        embed.set_footer(
            text=self.games[message.guild.id]["wikipedia"],
        )
        await message.channel.send(embed=embed)
        del self.games[message.channel.id]
