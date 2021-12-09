"""Games Cog for the "BotAToutFer" discord bot

(C) 2021 Clément SEIJIDO
Released under GNU General Public License v3.0 (GNU GPLv3)
e-mail clement@seijido.fr
"""

import os
import json
import re
import datetime
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import UserConverter

from game_controlers.hangman import Hangman
from game_controlers.quiz import Quiz


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

        self.pendu_games = {}  # {discord.TextChannel.id: Hangman, ...}
        # Path of the french scrabble dictionary
        self.DICTIONARY_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "ODS7.txt"
        )

        self.quiz_games = {}  # {discord.Guild.id: Quiz, ...}
        self.QUIZ_API_URL = "https://www.openquizzdb.org/api.php"
        self.QUIZ_API_PARAMETERS = {
            "key": self.bot.OPENQUIZZDB_TOKEN,
            "lang": "fr",
            "mono": "0",
            "anec": "1",
            "wiki": "1"
        }
        self.api_last_call = None
        self.quiz_semaphore = asyncio.Semaphore(1)
        self.quiz_colors = {
            "débutant": 0x00ff00,
            "confirmé": 0xffcc00,
            "expert": 0xff0000
        }

    @commands.command(
        name="pendu",
        help="Démarre une nouvelle partie de pendu"
    )
    async def pendu(self, ctx):
        if ctx.channel.id not in self.pendu_games:
            # If no game is currently running in this text channel
            try:
                game = Hangman(self.DICTIONARY_PATH)
                game.definition = self.get_word_definition(
                    ctx,
                    game.secret_word
                )

                # We add the game object in the class attribute "games"
                # linked with the id of the text channel
                self.pendu_games[ctx.channel.id] = game

                response = "Je lance une partie de pendu !\n" \
                           f"Vous avez {game.number_stroke} coup(s) pour " \
                           f"trouver le mot secret selon les règles du " \
                           f"pendu !\n" \
                           f"Voici le mot à deviner : "
                response += discord.utils.escape_markdown(game.visible_word)

            except Exception as e:
                self.bot.log.exception(
                    f"Unable to launch a hangman game in this channel: "
                    f"{ctx.channel.guild}, #{ctx.channel.name} "
                    f"({ctx.channel.id})",
                    exc_info=e
                )
                response = "Désolé, je n'ai pas réussi à lancer une partie. " \
                           "Veuillez réessayer."

        else:  # A game is currently running in this text channel
            game = self.pendu_games[ctx.channel.id]
            response = "Une partie est déjà en cours !\n" \
                       f"Il reste {game.number_stroke} coup(s) et voici le " \
                       f"mot à deviner : "
            response += discord.utils.escape_markdown(game.visible_word)

        await ctx.send(response)

    async def get_word_definition(self, ctx, word):
        try:
            self.bot.log.warning(f"Asking for word definition: {word}")
            url = f"https://api.dicolink.com/v1/mot/{word}/definitions"
            params = {
                "limite": "1",
                "api_key": self.bot.DICOLINK_TOKEN
            }
            async with self.bot.http_session.get(url=url, params=params) as r:
                # Retrieve a definition
                if r.status == 200:
                    response_content = await r.json()
                    return response_content[0]["definition"]
        except Exception as e:
            self.bot.log.exception(
                f"Unable to load a word definition in this channel: "
                f"{ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})",
                exc_info=e
            )
            return "Désolé, je n'ai pas trouvé cette définition..."

    @commands.command(
        name="pendu-status",
        help="Affiche le status de la partie en cours"
    )
    async def pendu_status(self, ctx):
        if ctx.channel.id in self.pendu_games:
            # If a game is currently running in this text channel
            game = self.pendu_games[ctx.channel.id]
            response = "Le mot à deviner : " \
                       f"{discord.utils.escape_markdown(game.visible_word)}" \
                       "\n" \
                       f"Les lettres déjà proposées : " \
                       f"{game.get_guessed_letters()}\n" \
                       f"\nLe pendu :\n```\n{game.drawing()}\n```"

        else:
            response = "Aucune partie de pendu n'est en cours ! Mais vous " \
                       "pouvez en lancer une avec la commande '!pendu'"

        await ctx.send(response)

    @commands.command(name="pendu-stop", help="Arrête la partie en cours")
    async def pendu_stop(self, ctx):
        if ctx.channel.id in self.pendu_games:
            # If a game is currently running in this text channel
            response = "Ohhh, dommage, mais je comprend que vous souhaitez " \
                       "arrêter. Voici le mot qui était à deviner : " \
                       f"{self.pendu_games[ctx.channel.id].secret_word}"
            del self.pendu_games[ctx.channel.id]

        else:
            response = "Aucune partie de pendu n'est en cours ! Mais vous " \
                       "pouvez en lancer une avec la commande '!pendu'"

        await ctx.send(response)

    @commands.Cog.listener('on_message')
    async def pendu_process_game(self, message):
        if not re.match(r"^[a-z]$", message.content, flags=re.IGNORECASE):
            # the message is not a single letter
            return

        if message.channel.id not in self.pendu_games:
            # If no game is currently running in this text channel
            return

        ctx = await self.bot.get_context(message)
        game = self.pendu_games[ctx.channel.id]
        user_guess = message.content.upper()

        if user_guess in game.guessed_letters:
            # If the guessed letter has already been guessed
            response = f"Vous avez déjà demandé la lettre {user_guess} !"

            await ctx.send(response)
            await self.pendu_status(ctx)  # reminder players the game status

        elif user_guess in game.secret_word:
            # If the guessed letter is in the secret word
            response = "Oui !"
            # Add the letter to the guessed letters list
            game.guessed_letters.append(user_guess)
            # Modify the visible word
            game.process_visible_word(user_guess)

            if game.visible_word == game.secret_word:  # WIN
                # Game duration in seconds
                game_duration = datetime.timedelta(
                    seconds=(
                        datetime.datetime.now() - game.starting_time
                    ).seconds
                )

                response += " C'est gagné ! Vous avez deviné le mot " \
                            f"{game.secret_word} ({game.definition})\n" \
                            f"Durée de la partie : {game_duration}"

                self.save_pendu_score(
                    str(ctx.guild.id),
                    str(ctx.author.id),
                    game_duration.seconds
                )

                del self.pendu_games[ctx.channel.id]  # Delete the current game
                await ctx.send(response)
                return

            await ctx.send(response)
            await self.pendu_status(ctx)

        else:  # If the guessed letter is not in the secret word
            response = "Non !"

            # Add the letter to the guessed letters list
            game.guessed_letters.append(user_guess)
            # Decrement the stroke number
            game.number_stroke -= 1

            if game.number_stroke == 0:  # LOSE
                response += f" C'est perdu !\n```\n{game.drawing()}\n```\n" \
                            f"Le mot à deviner était : {game.secret_word} " \
                            f"({game.definition})"

                del self.pendu_games[ctx.channel.id]  # Delete the current game
                await ctx.send(response)
                return

            await ctx.send(response)
            await self.pendu_status(ctx)

    def save_pendu_score(self, guild_id: str, author_id: str, game_duration):
        try:
            with open(self.SCORE_PATH, "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error("No score.json file: ", exc_info=e)
            scores = {
                "pendu": {},
                "quiz": {}
            }

        if guild_id in scores["pendu"]:
            if author_id in scores["pendu"][guild_id]:
                if game_duration < scores["pendu"][guild_id][author_id]:
                    scores["pendu"][guild_id][author_id] = game_duration
            else:
                scores["pendu"][guild_id][author_id] = game_duration
        else:
            scores["pendu"][guild_id] = {author_id: game_duration}

        with open(self.SCORE_PATH, "w", encoding="utf8") as f:
            json.dump(scores, f, indent=4)

    @commands.command(
        name="quiz",
        help="Demande une question du quiz. Option, choix du niveau "
             "de difficulté (1=débutant, 2=confirmé, 3=expert)"
    )
    async def quiz(self, ctx, option=""):
        if ctx.guild.id not in self.quiz_games:
            # If no game is currently running in this text channel
            await self.launch_quiz(ctx, option)
        else:
            game = self.quiz_games[ctx.guild.id]
            if game.ready:
                await ctx.send(embed=self.create_quiz_embed(game))

    def create_quiz_embed(self, game):
        embed = discord.Embed(
            title=f"Quiz - Catégorie {game.category} ({game.difficulty})",
            description=game.question,
            color=self.quiz_colors[game.difficulty]
        )

        if game.hint:
            for other_choice in game.other_choices:
                embed.add_field(
                    name="Proposition",
                    value=other_choice,
                    inline=True
                )

        return embed

    @commands.command(
        name="quiz-indice",
        help="Demander les 4 propositions de réponse à la question en cours"
    )
    async def quiz_indice(self, ctx):
        if ctx.guild.id in self.quiz_games:
            # If a game is currently running in this text channel
            game = self.quiz_games[ctx.guild.id]
            if game.ready:
                game.hint = True
                await ctx.send(embed=self.create_quiz_embed(game))
        else:
            await ctx.send("Il n'y a pas de quiz en cours dans ce serveur !")

    @commands.command(
        name="quiz-stop",
        help="Annule la question de quiz en cours"
    )
    async def quiz_stop(self, ctx):
        if ctx.guild.id in self.quiz_games:
            # If a game is currently running in this text channel
            game = self.quiz_games[ctx.guild.id]
            if game.ready:
                embed = discord.Embed(
                    title="Quiz - Fin de la question",
                    description=game.correct_answer
                )
                embed.add_field(
                    name="Anecdote",
                    value=game.anecdote,
                    inline=True
                )
                embed.set_footer(
                    text=game.wikipedia
                )

                await ctx.send(embed=embed)
                del self.quiz_games[ctx.guild.id]
        else:
            await ctx.send("Il n'y a pas de quiz en cours dans ce serveur !")

    @commands.Cog.listener('on_message')
    async def quiz_process_game(self, message):
        if message.guild.id in self.quiz_games \
                and self.quiz_games[message.guild.id].ready:
            game = self.quiz_games[message.guild.id]
            if game.cleaned_response in Quiz.clean_response(message.content):
                await self.quiz_win(message)

    async def launch_quiz(self, ctx, option):
        game = Quiz()
        self.quiz_games[ctx.guild.id] = game
        now = datetime.datetime.now()
        if self.api_last_call and (now - self.api_last_call).seconds < 65:
            response = "J'envoie une question dans quelques secondes !"
            await ctx.send(response)

        if option in ["facile", "débutant", "debutant", "1"]:
            params = dict(self.QUIZ_API_PARAMETERS, **{"diff": "1"})
        elif option in ["moyen", "confirmé", "confirme", "2"]:
            params = dict(self.QUIZ_API_PARAMETERS, **{"diff": "2"})
        elif option in ["difficile", "expert", "3"]:
            params = dict(self.QUIZ_API_PARAMETERS, **{"diff": "3"})
        else:
            params = self.QUIZ_API_PARAMETERS

        async with self.quiz_semaphore:
            self.bot.log.warning("Asking for a quiz question")
            async with self.bot.http_session.get(
                    url=self.QUIZ_API_URL, params=params) as r:
                self.api_last_call = datetime.datetime.now()
                if r.status == 200:
                    try:
                        question = await r.json()
                    except json.decoder.JSONDecodeError as e:
                        self.bot.log.exception(
                            f"Unable to decode API response in this channel: "
                            f"{ctx.channel.guild}, #{ctx.channel.name} "
                            f"({ctx.channel.id})",
                            exc_info=e
                        )
                        response = "Erreur d'API, merci de réessayer"
                        await ctx.send(response)
                    else:
                        if question["response_code"] == 0:  # Succès
                            game.start(question["results"][0])
                            await ctx.send(embed=self.create_quiz_embed(game))
                        else:
                            self.bot.log.error(
                                f"Problem with the API key, code: "
                                f"{question['response_code']}"
                            )
                            response = "Désolé, je n'ai pas réussi à " \
                                       "trouver une question de quiz..."
                            await ctx.send(response)

            execution_time = (
                    datetime.datetime.now() - self.api_last_call
                ).seconds
            if execution_time < 65:
                # keep the semaphore for one minute
                await asyncio.sleep(65 - execution_time)

    async def quiz_win(self, message):
        game = self.quiz_games[message.guild.id]
        points = 0
        if game.difficulty == "débutant":
            points = 2
        elif game.difficulty == "confirmé":
            points = 4
        elif game.difficulty == "expert":
            points = 6

        if game.hint:
            points = int(points/2)

        self.save_quiz_score(
            str(message.guild.id),
            str(message.author.id),
            points
        )

        embed = discord.Embed(
            title="Quiz - Fin de la question",
            description=f"Bravo {message.author.name}. "
                        f"La réponse était {game.correct_answer}. "
                        f"{points} point(s) !",
            color=self.quiz_colors[game.difficulty]
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        embed.add_field(
            name="Anecdote",
            value=game.anecdote,
            inline=True
        )
        embed.set_footer(
            text=game.wikipedia,
        )
        await message.channel.send(embed=embed)
        del self.quiz_games[message.guild.id]

    def save_quiz_score(self, guild_id: str, author_id: str, points):
        try:
            with open(self.SCORE_PATH, "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error("No score.json file: ", exc_info=e)
            scores = {
                "pendu": {},
                "quiz": {}
            }

        if guild_id in scores["quiz"]:
            if author_id in scores["quiz"][guild_id]:
                scores["quiz"][guild_id][author_id] += points
            else:
                scores["quiz"][guild_id][author_id] = points
        else:
            scores["quiz"][guild_id] = {author_id: points}

        with open(self.SCORE_PATH, "w", encoding="utf8") as f:
            json.dump(scores, f, indent=4)

    @commands.command(name="scores", help="Affiche les scores des jeux")
    async def scores(self, ctx):
        try:
            with open(self.SCORE_PATH, "r") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error("No score.json file: ", exc_info=e)
            response = "Il n'y a pas de scores enregistrés !"
            await ctx.send(response)
            return

        if str(ctx.guild.id) in scores["pendu"]:
            user_scores = scores["pendu"][str(ctx.guild.id)]
            user_scores = sorted(user_scores.items(), key=lambda x: x[1])

            description = ""
            for user_id, score in user_scores:
                try:
                    user = await UserConverter().convert(ctx, user_id)
                except discord.ext.commands.UserNotFound as e:
                    self.bot.log.error(
                        f"user {user_id} not found in {ctx.guild.id}",
                        exc_info=e
                    )
                else:
                    description += f"{user.name} : {score} secondes\n"
        else:
            description = "Il n'y a pas de scores de pendu dans ce serveur !"

        embed = discord.Embed(
            title="Voici les scores du pendu !",
            description=description
        )

        await ctx.send(embed=embed)

        if str(ctx.guild.id) in scores["quiz"]:
            user_scores = scores["quiz"][str(ctx.guild.id)]
            user_scores = sorted(
                user_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )

            description = ""
            for user_id, score in user_scores[:10]:
                try:
                    user = await UserConverter().convert(ctx, user_id)
                except discord.ext.commands.UserNotFound as e:
                    self.bot.log.error(
                        f"user {user_id} not found in {ctx.guild.id}",
                        exc_info=e
                    )
                else:
                    description += f"{user.name} : {score} secondes\n"
        else:
            description = "Il n'y a pas de scores de quiz dans ce serveur !"

        embed = discord.Embed(
            title="Voici les scores du quiz !",
            description=description
        )

        await ctx.send(embed=embed)
