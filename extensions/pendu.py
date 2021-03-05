# hanged commands for BotÀToutFer
import os
import random
import json
import re
import aiohttp
import datetime

from discord.ext import commands


def setup(bot):
    bot.add_cog(Pendu(bot))


class Pendu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        self.games = {}
        # games = {discord.TextChannel.id: {
        #     "secret_word": "",
        #     "visible_word": "",
        #     "number_stroke": 10,
        #     "gessed_letters": [],
        #     "definition": "",
        #     "starting_time": datetime.datetime
        # }}

        # Path of the french scrabble dictionary
        self.DICTIONARY_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "ODS7.txt"
        )

    @commands.command(name="pendu", help="Joue au pendu")
    async def pendu(self, ctx, option: str="help"):
        option = option.casefold().strip()

        if option == "status":
            await self.status(ctx)

        elif option == "start":
            await self.start(ctx)

        elif option == "stop":
            await self.stop(ctx)

        elif option == "restart" or option == "reboot":
            await self.restart(ctx)

        elif re.match(r"^[a-z]$", option):
            await self.guess(ctx, option)

        else:  # Display help
            response = (
                "Les commandes du jeu du pendu :\n```\n"
                + "!pendu start                       "
                + "Lance une partie\n"
                + "!pendu stop                        "
                + "Arrête la partie en cours\n"
                + "!pendu restart (ou !pendu reboot)  "
                + "Arrête la partie en cours et en relance une\n"
                + "!pendu status                      "
                + "Affiche le status de la partie en cours\n"
                + "!pendu <lettre>                    "
                + "Proposer une lettre\n```"
            )
            await ctx.send(response)

    async def status(self, ctx):
        if ctx.channel.id in self.games:
            visible_word = self.games[ctx.channel.id]["visible_word"]
            response = (
                "Le mot à deviner : "
                + visible_word.replace("*", "\*")
                + "\nLes lettres déjà proposées : "
            )
            for letter in self.games[ctx.channel.id]["gessed_letters"]:
                response += f"{letter} "
            response += (
                "\nLe pendu :\n```\n"
                + self.hanged_drawing(
                    self.games[ctx.channel.id]["number_stroke"]
                )
                + "\n```"
            )
            await ctx.send(response)
        else:
            await self.no_game(ctx)

    async def start(self, ctx):
        if ctx.channel.id not in self.games:
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
                game["gessed_letters"] = []
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
                            # Retreve a definition
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

                # We add the game dictionary in the class atribute "games"
                # linked with the id of the text channel
                self.games[ctx.channel.id] = game

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
            visible_word = self.games[ctx.channel.id]["visible_word"]
            response = (
                f"Une partie est déjà en cours !\n"
                + f"Il reste {self.games[ctx.channel.id]['number_stroke']} "
                + "coup(s) et voici le mot à deviner : "
                + visible_word.replace("*", "\*")
            )
        await ctx.send(response)

    async def stop(self, ctx):
        if ctx.channel.id in self.games:
            # If a game is currently running in this text channel
            response = (
                "Ohhh, dommage, mais je comprend que vous souhaitez arrêter. "
                + "Voici le mot qui était à deviner : "
                + f"{self.games[ctx.channel.id]['secret_word']}"
            )
            del self.games[ctx.channel.id]
            await ctx.send(response)
        else:  # No game is currently running in this text channel
            await self.no_game(ctx)

    async def no_game(self, ctx):
        response = (
            "Aucune partie de pendu n'est en cours ! "
            + "Mais vous pouvez en lancer une avec la commande '!pendu start'"
        )
        await ctx.send(response)

    async def restart(self, ctx):
        if ctx.channel.id in self.games:
            # If a game is currently running in this text channel
            response = (
                "Bon, on recommence. Mais juste pour info, "
                + "le mot précédent à deviner était : "
                + f"{self.games[ctx.channel.id]['secret_word']} "
                + f"({self.games[ctx.channel.id]['definition']})"
            )
            del self.games[ctx.channel.id]  # Delete the current game
            await ctx.send(response)

        await self.start(ctx)

    async def guess(self, ctx, option):
        if ctx.channel.id in self.games:
            # If a game is currently running in this text channel
            response = ""
            guessed_letters = []  # Clean list of guessed letters
            for letters in self.games[ctx.channel.id]["gessed_letters"]:
                guessed_letters.append(
                    re.findall(r"[a-z]", element, flags=re.IGNORECASE)[0]
                )

            if option in guessed_letters:
                # If the gessed letter has already been guessed
                response = f"Vous avez déjà demandé la lettre {option} !"

            elif option in self.games[ctx.channel.id]["secret_word"]:
                # If the gessed letter is in the secret word
                response = "Oui !"
                # Add the letter to the gessed letters list
                self.games[ctx.channel.id]["gessed_letters"].append(option)

                length_secret_word = len(
                    self.games[ctx.channel.id]["secret_word"]
                )
                for i in range(length_secret_word):
                    # Replace the guessed letter in the visible word
                    if self.games[ctx.channel.id]["secret_word"][i] == option:
                        self.games[ctx.channel.id]["visible_word"] = (
                            self.games[ctx.channel.id]["visible_word"][:i]
                            + option
                            + self.games[ctx.channel.id]["visible_word"][i+1:]
                        )

                if (self.games[ctx.channel.id]["visible_word"]
                        == self.games[ctx.channel.id]["secret_word"]):  # WIN
                    # Game duration in seconds
                    game_duration = datetime.timedelta(
                        seconds=(
                            datetime.datetime.now()
                            - self.games[ctx.channel.id]['starting_time']
                        ).seconds
                    )
                    response += (
                        " C'est gagné ! Vous avez deviné le mot "
                        + f"{self.games[ctx.channel.id]['secret_word']} "
                        + f"({self.games[ctx.channel.id]['definition']})\n"
                        + f"Durée de la partie : {game_duration}"
                    )
                    del self.games[ctx.channel.id]  # Delete the current game
                    await ctx.send(response)
                    return

            else:  # If the guessed letter is not in the secret word
                response = "Non !"

                # Add the letter to the gessed letters list
                self.games[ctx.channel.id]["gessed_letters"].append(
                    f"~~{option}~~"
                )
                # Decrement the stroke number
                self.games[ctx.channel.id]["number_stroke"] -= 1

                if self.games[ctx.channel.id]["number_stroke"] == 0:  # LOSE
                    response += (
                        " C'est perdu !"
                        + "\n```\n"
                        + self.hanged_drawing(
                            self.games[ctx.channel.id]["number_stroke"]
                        )
                        + "\n```\n"
                        + "Le mot à deviner était : "
                        + f"{self.games[ctx.channel.id]['secret_word']} "
                        + f"({self.games[ctx.channel.id]['definition']})"
                    )
                    del self.games[ctx.channel.id]  # Delete the current game
                    await ctx.send(response)
                    return

            await ctx.send(response)
            await self.status(ctx)

        else:  # No game is currently running in this text channel
            await self.no_game(ctx)

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
