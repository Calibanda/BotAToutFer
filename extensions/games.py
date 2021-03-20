# games commands for BotÀToutFer
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
    bot.add_cog(Games(bot))


class Games(commands.Cog, name="Jeux"):
    def __init__(self, bot):
        self.bot = bot

        self.SCORE_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "scores.json"
        )

        self.pendu_games = {}
        # pendu_games = {discord.TextChannel.id: {
        #     "secret_word": "",
        #     "visible_word": "",
        #     "number_stroke": 10,
        #     "guessed_letters": [],
        #     "definition": "",
        #     "starting_time": datetime.datetime
        # }}

        # Path of the french scrabble dictionary
        self.DICTIONARY_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "ODS7.txt"
        )

        self.quiz_games = {}
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

    @commands.command(name="pendu", help="Démarre une nouvelle partie de pendu")
    async def pendu(self, ctx):
        if ctx.channel.id not in self.pendu_games:
            # If no game is currently running in this text channel
            try:
                game = {}  # Creating a new dictionary

                with open(self.DICTIONARY_PATH, "r", encoding="utf-8") as f:
                    # Chose a secret word in the dictionary
                    word = random.choice(f.readlines())
                    game["secret_word"] = word.casefold().strip()

                # Creating a word with "*" that will be displayed to players
                game["visible_word"] = "*" * len(game["secret_word"])
                # Players have 10 strokes to find the word
                game["number_stroke"] = 10
                # Create the list to store all the guessed letters
                game["guessed_letters"] = []
                # The definition of the word
                game["definition"] = (
                    "Désolé, je n'ai pas trouvé cette définition..."
                )

                try:
                    async with aiohttp.ClientSession() as session:
                        self.bot.log.warning(f"Asking for word definition")
                        url = (
                            "https://api.dicolink.com/v1/mot/"
                            + f"{game['secret_word']}/definitions"
                            + f"?limite=1&api_key={self.bot.DICOLINK_TOKEN}"
                        )
                        async with session.get(url) as r:
                            # Retrieve a definition
                            if r.status == 200:
                                definit = await r.json()
                                game["definition"] = definit[0]["definition"]
                except Exception as e:
                    self.bot.log.exception(
                        (
                            "Unable to load a word definition in "
                            + f"this channel: {ctx.channel.guild}, "
                            + f"#{ctx.channel.name} ({ctx.channel.id})"
                        ),
                        exc_info=e
                    )

                # We save the datetime of the start of the game
                game["starting_time"] = datetime.datetime.now()

                # We add the game dictionary in the class attribute "games"
                # linked with the id of the text channel
                self.pendu_games[ctx.channel.id] = game

                response = (
                    "Je lance une partie de pendu !\n"
                    + f"Vous avez {game['number_stroke']} coup(s) pour "
                    + "trouver le mot secret selon les règles du pendu !\n"
                    + "Voici le mot à deviner : "
                    + game["visible_word"].replace("*", "\*")
                )

            except Exception as e:
                self.bot.log.exception(
                    (
                        "Unable to launch a 'pendu' game in this channel: "
                        + f"{ctx.channel.guild}, "
                        + f"#{ctx.channel.name} ({ctx.channel.id})"
                    ),
                    exc_info=e
                )
                response = (
                    "Désolé, je n'ai pas réussi à lancer une partie. "
                    + "Veuillez réessayer."
                )

        else:  # A game is currently running in this text channel
            visible_word = self.pendu_games[ctx.channel.id]["visible_word"]
            response = (
                f"Une partie est déjà en cours !\n"
                + f"Il reste {self.pendu_games[ctx.channel.id]['number_stroke']} "
                + "coup(s) et voici le mot à deviner : "
                + visible_word.replace("*", "\*")
            )
        await ctx.send(response)

    @commands.command(name="pendu-status", help="Affiche le status de la partie en cours")
    async def pendu_status(self, ctx):
        if ctx.channel.id in self.pendu_games:
            visible_word = self.pendu_games[ctx.channel.id]["visible_word"]
            response = (
                "Le mot à deviner : "
                + visible_word.replace("*", "\*")
                + "\nLes lettres déjà proposées : "
            )
            for letter in self.pendu_games[ctx.channel.id]["guessed_letters"]:
                response += f"{letter} "
            response += (
                "\nLe pendu :\n```\n"
                + self.hanged_drawing(self.pendu_games[ctx.channel.id]["number_stroke"])
                + "\n```"
            )
            await ctx.send(response)
        else:
            await self.no_pendu_game(ctx)

    @commands.command(name="pendu-stop", help="Arrête la partie en cours")
    async def pendu_stop(self, ctx):
        if ctx.channel.id in self.pendu_games:
            # If a game is currently running in this text channel
            response = (
                "Ohhh, dommage, mais je comprend que vous souhaitez arrêter. "
                + "Voici le mot qui était à deviner : "
                + f"{self.pendu_games[ctx.channel.id]['secret_word']}"
            )
            del self.pendu_games[ctx.channel.id]
            await ctx.send(response)
        else:  # No game is currently running in this text channel
            await self.no_pendu_game(ctx)

    @commands.Cog.listener('on_message')
    async def pendu_process_game(self, message):
        if message.channel.id in self.pendu_games and re.match(r"^[a-z]$", message.content):
            # If a game is currently running in this text channel
            ctx = await self.bot.get_context(message)
            guessed_letters = []  # Clean list of guessed letters
            for letters in self.pendu_games[ctx.channel.id]["guessed_letters"]:
                guessed_letters.append(
                    re.findall(r"[a-z]", letters, flags=re.IGNORECASE)[0]
                )

            if message.content in guessed_letters:
                # If the guessed letter has already been guessed
                response = f"Vous avez déjà demandé la lettre {message.content} !"

            elif message.content in self.pendu_games[ctx.channel.id]["secret_word"]:
                # If the guessed letter is in the secret word
                response = "Oui !"
                # Add the letter to the guessed letters list
                self.pendu_games[ctx.channel.id]["guessed_letters"].append(message.content)

                length_secret_word = len(
                    self.pendu_games[ctx.channel.id]["secret_word"]
                )
                for i in range(length_secret_word):
                    # Replace the guessed letter in the visible word
                    if self.pendu_games[ctx.channel.id]["secret_word"][i] == message.content:
                        self.pendu_games[ctx.channel.id]["visible_word"] = (
                            self.pendu_games[ctx.channel.id]["visible_word"][:i]
                            + message.content
                            + self.pendu_games[ctx.channel.id]["visible_word"][i + 1:]
                        )

                if (self.pendu_games[ctx.channel.id]["visible_word"]
                        == self.pendu_games[ctx.channel.id]["secret_word"]):  # WIN
                    # Game duration in seconds
                    game_duration = datetime.timedelta(
                        seconds=(
                            datetime.datetime.now()
                            - self.pendu_games[ctx.channel.id]['starting_time']
                        ).seconds
                    )
                    response += (
                        " C'est gagné ! Vous avez deviné le mot "
                        + f"{self.pendu_games[ctx.channel.id]['secret_word']} "
                        + f"({self.pendu_games[ctx.channel.id]['definition']})\n"
                        + f"Durée de la partie : {game_duration}"
                    )

                    self.save_pendu_score(ctx.guild.id, ctx.author.id, game_duration)

                    del self.pendu_games[ctx.channel.id]  # Delete the current game
                    await ctx.send(response)
                    return

            else:  # If the guessed letter is not in the secret word
                response = "Non !"

                # Add the letter to the guessed letters list
                self.pendu_games[ctx.channel.id]["guessed_letters"].append(
                    f"~~{message.content}~~"
                )
                # Decrement the stroke number
                self.pendu_games[ctx.channel.id]["number_stroke"] -= 1

                if self.pendu_games[ctx.channel.id]["number_stroke"] == 0:  # LOSE
                    response += (
                        " C'est perdu !"
                        + "\n```\n"
                        + self.hanged_drawing(
                            self.pendu_games[ctx.channel.id]["number_stroke"]
                        )
                        + "\n```\n"
                        + "Le mot à deviner était : "
                        + f"{self.pendu_games[ctx.channel.id]['secret_word']} "
                        + f"({self.pendu_games[ctx.channel.id]['definition']})"
                    )
                    del self.pendu_games[ctx.channel.id]  # Delete the current game
                    await ctx.send(response)
                    return

            await ctx.send(response)
            await self.pendu_status(ctx)

    async def no_pendu_game(self, ctx):
        response = (
            "Aucune partie de pendu n'est en cours ! "
            + "Mais vous pouvez en lancer une avec la commande '!pendu start'"
        )
        await ctx.send(response)

    def hanged_drawing(self, number_stroke):
        if number_stroke == 10:
            return ""
        elif number_stroke == 9:
            return "___"
        elif number_stroke == 8:
            return " |\n |\n |\n |\n |\n_|_"
        elif number_stroke == 7:
            return " ____________\n |\n |\n |\n |\n |\n_|_"
        elif number_stroke == 6:
            return " ____________\n |/\n |\n |\n |\n |\n_|_"
        elif number_stroke == 5:
            return " ____________\n |/     |\n |\n |\n |\n |\n_|_"
        elif number_stroke == 4:
            return " ____________\n |/     |\n |      O\n |\n |\n |\n_|_"
        elif number_stroke == 3:
            return (
                " ____________\n |/     |\n |      O\n |      |\n |      "
                + "|\n |\n_|_"
            )
        elif number_stroke == 2:
            return (
                " ____________\n |/     |\n |      O\n |     _|_\n |      "
                + "|\n |\n_|_"
            )
        elif number_stroke == 1:
            return (
                " ____________\n |/     |\n |      O\n |     _|_\n |      "
                + "|\n |     /\n_|_"
            )
        elif number_stroke == 0:
            return (
                " ____________\n |/     |\n |      O\n |     _|_\n |      "
                + "|\n |     / \\ \n_|_"
            )

    @commands.command(name="quiz", help="Demande une question du quiz")
    async def quiz(self, ctx):
        if ctx.guild.id in self.quiz_games:
            if "question" in self.quiz_games[ctx.guild.id]:
                await self.send_quiz_question(ctx)
        else:
            await self.launch_quiz(ctx)

    @commands.command(name="quiz-indice", help="Demander les 4 propositions de réponse à la question en cours")
    async def quiz_indice(self, ctx):
        if ctx.guild.id in self.quiz_games:
            if "question" in self.quiz_games[ctx.guild.id]:
                self.quiz_games[ctx.guild.id]["indice"] = True
                await self.send_quiz_question(ctx)
        else:
            await ctx.send("Il n'y a pas de quiz en cours dans ce serveur !")

    @commands.command(name="quiz-stop", help="Annule la question de quiz en cours")
    async def quiz_stop(self, ctx):
        if ctx.guild.id in self.quiz_games:
            if "question" in self.quiz_games[ctx.guild.id]:
                title = "Quiz - Fin de la question"
                description = self.quiz_games[ctx.guild.id]["reponse_correcte"]
                embed = discord.Embed(title=title, description=description)
                embed.add_field(
                    name="Anecdote",
                    value=self.quiz_games[ctx.guild.id]["anecdote"],
                    inline=True
                )
                embed.set_footer(
                    text=self.quiz_games[ctx.guild.id]["wikipedia"],
                )
                await ctx.send(embed=embed)
                del self.quiz_games[ctx.guild.id]
        else:
            await ctx.send("Il n'y a pas de quiz en cours dans ce serveur !")

    @commands.Cog.listener('on_message')
    async def quiz_process_game(self, message):
        if message.guild.id in self.quiz_games and "question" in self.quiz_games[message.guild.id]:
            if self.quiz_games[message.guild.id]["clean_response"] in self.remove_accents(message.content.casefold().strip()):
                await self.quiz_win(message)

    async def launch_quiz(self, ctx):
        self.quiz_games[ctx.guild.id] = {}
        if self.api_last_call:
            delta = (datetime.datetime.now() - self.api_last_call).seconds
            if delta < 65:
                response = f"J'envoie une question dans {65 - delta} seconde(s) !"
                await ctx.send(response)
                await asyncio.sleep(65 - delta)

        async with aiohttp.ClientSession() as session:
            self.bot.log.warning(f"Asking for a quiz question")
            async with session.get(self.API_URL, params=self.API_PARAMETERS) as r:
                if r.status == 200:
                    self.api_last_call = datetime.datetime.now()
                    question = await r.json()
                    if question["response_code"] == 0:  # Succès
                        self.quiz_games[ctx.guild.id] = question["results"][0]
                        self.quiz_games[ctx.guild.id]["starting_time"] = datetime.datetime.now()
                        random.shuffle(self.quiz_games[ctx.guild.id]["autres_choix"])
                        self.quiz_games[ctx.guild.id]["clean_response"] = self.clean_response(self.quiz_games[ctx.guild.id]["reponse_correcte"])
                        self.quiz_games[ctx.guild.id]["indice"] = False
                        await self.send_quiz_question(ctx)
                    else:
                        self.bot.log.error(f"Problem with the API key, code: {question['response_code']}")
                        response = "Désolé, je n'ai pas réussi à trouver une question de quiz..."
                        await ctx.send(response)

    def clean_response(self, response):
        response = response.casefold().strip()

        if response[0] == "'":
            response = response[1:]
        if response[-1] == "'":
            response = response[:-1]

        stop_words = [
            "le",
            "la",
            "les",
            "un",
            "une",
            "des"
        ]
        response = " ".join([word for word in response.split(" ") if word not in stop_words])

        response = self.remove_accents(response)

        return response

    def remove_accents(self, text):
        return text.replace("à", "a")\
            .replace("â", "a")\
            .replace("ä", "a")\
            .replace("ç", "c")\
            .replace("é", "e")\
            .replace("è", "e")\
            .replace("ê", "e")\
            .replace("ë", "e")\
            .replace("î", "i")\
            .replace("ï", "i")\
            .replace("ô", "o")\
            .replace("ö", "o")\
            .replace("ù", "u")\
            .replace("û", "u")\
            .replace("ü", "u")\
            .replace("ÿ", "y")\
            .replace("œ", "oe")\
            .replace("’", "'")

    async def send_quiz_question(self, ctx):
        title = "Quiz - Catégorie " + self.quiz_games[ctx.guild.id]["categorie"] + " (" + self.quiz_games[ctx.guild.id]["difficulte"] + ")"
        colors = {
            "débutant": 0x00ff00,
            "confirmé": 0xffcc00,
            "expert": 0xff0000
        }
        description = self.quiz_games[ctx.guild.id]["question"]
        embed = discord.Embed(
            title=title,
            description=description,
            color=colors[self.quiz_games[ctx.guild.id]["difficulte"]]
        )
        if self.quiz_games[ctx.guild.id]["indice"]:
            for autre_choix in self.quiz_games[ctx.guild.id]["autres_choix"]:
                embed.add_field(
                    name="Proposition",
                    value=autre_choix,
                    inline=True
                )
        await ctx.send(embed=embed)

    async def quiz_win(self, message):
        title = "Quiz - Fin de la question"
        points = 0
        if self.quiz_games[message.guild.id]["difficulte"] == "débutant":
            points = 2
        elif self.quiz_games[message.guild.id]["difficulte"] == "confirmé":
            points = 4
        elif self.quiz_games[message.guild.id]["difficulte"] == "expert":
            points = 6

        if self.quiz_games[message.guild.id]["indice"]:
            points = int(points/2)

        self.save_quiz_score(message.guild.id, message.author.id, points)

        description = f"Bravo {message.author.name}. La réponse était " + self.quiz_games[message.guild.id]["reponse_correcte"] + f". {points} point(s) !"
        colors = {
            "débutant": 0x00ff00,
            "confirmé": 0xffcc00,
            "expert": 0xff0000
        }
        embed = discord.Embed(
            title=title,
            description=description,
            color=colors[self.quiz_games[message.guild.id]["difficulte"]]
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        embed.add_field(
            name="Anecdote",
            value=self.quiz_games[message.guild.id]["anecdote"],
            inline=True
        )
        embed.set_footer(
            text=self.quiz_games[message.guild.id]["wikipedia"],
        )
        await message.channel.send(embed=embed)
        del self.quiz_games[message.guild.id]

    def save_pendu_score(self, guild_id, author_id, game_duration):
        try:
            with open(self.SCORE_PATH, "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error(f"Caught exception:", exc_info=e)
            scores = {
                "pendu": {},
                "quiz": {}
            }

        if str(guild_id) in scores["pendu"]:
            if str(author_id) in scores["pendu"][str(guild_id)]:
                if game_duration.seconds < scores["pendu"][str(guild_id)][str(author_id)]:
                    scores["pendu"][str(guild_id)][str(author_id)] = game_duration.seconds
            else:
                scores["pendu"][str(guild_id)][str(author_id)] = game_duration.seconds
        else:
            scores["pendu"][str(guild_id)] = {str(author_id): game_duration.seconds}

        with open(self.SCORE_PATH, "w", encoding="utf8") as f:
            json.dump(scores, f, indent=4)

    def save_quiz_score(self, guild_id, author_id, points):
        try:
            with open(self.SCORE_PATH, "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error(f"Caught exception:", exc_info=e)
            scores = {
                "pendu": {},
                "quiz": {}
            }

        if str(guild_id) in scores["quiz"]:
            if str(author_id) in scores["quiz"][str(guild_id)]:
                scores["quiz"][str(guild_id)][str(author_id)] += points
            else:
                scores["quiz"][str(guild_id)][str(author_id)] = points
        else:
            scores["quiz"][str(guild_id)] = {str(author_id): points}

        with open(self.SCORE_PATH, "w", encoding="utf8") as f:
            json.dump(scores, f, indent=4)

    @commands.command(name="scores", help="Affiche les scores des jeux")
    async def scores(self, ctx):
        try:
            with open(self.SCORE_PATH, "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error(f"Caught exception:", exc_info=e)
        else:
            if str(ctx.guild.id) in scores["pendu"]:
                user_scores = scores["pendu"][str(ctx.guild.id)]
                user_scores = sorted(user_scores.items(), key=lambda x: x[1])

                description = ""
                for user_id, score in user_scores:
                    description += self.bot.get_user(user_id).name + " : " + str(score) + " secondes\n"
            else:
                description = "Il n'y a pas de scores de pendu dans ce serveur !"

            embed = discord.Embed(
                title="Voici les scores du pendu !",
                description=description
            )

            await ctx.send(embed=embed)

            if str(ctx.guild.id) in scores["quiz"]:
                user_scores = scores["quiz"][str(ctx.guild.id)]
                user_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

                description = ""
                for user_id, score in user_scores[:10]:
                    description += self.bot.get_user(
                        user_id).name + " : " + str(score) + " points\n"
            else:
                description = "Il n'y a pas de scores de quiz dans ce serveur !"

            embed = discord.Embed(
                title="Voici les scores du quiz !",
                description=description
            )

            await ctx.send(embed=embed)
