# hanged commands for BotAToutFer
import os
import random
import json
import re
import aiohttp
import datetime

from discord.ext import commands

import const


class Pendu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        self.current_games = {} # {discord.TextChannel.id: {"secret_word": "", "visible_word": "", "number_stroke": 10, "gessed_letters": [], "definition": "", "starting_time": datetime.datetime}}


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

        else: # Display help
            response = "Les commandes du jeu du pendu :\n```\n!pendu start                       Lance une partie\n!pendu stop                        Arrête la partie en cours\n!pendu restart (ou !pendu reboot)  Arrête la partie en cours et en relance une\n!pendu status                      Affiche le status de la partie en cours\n!pendu <lettre>                    Proposer une lettre\n```"
            await ctx.send(response)


    async def status(self, ctx):
        if ctx.channel.id in self.current_games:
            response = "Le mot à deviner : " + self.current_games[ctx.channel.id]["visible_word"].replace("*", "\*") + "\nLes lettres déjà proposées : "
            for letter in self.current_games[ctx.channel.id]["gessed_letters"]:
                response += f"{letter} "
            response += "\nLe pendu :\n```\n" + self.hanged_drawing(self.current_games[ctx.channel.id]["number_stroke"]) + "\n```"
            await ctx.send(response)
        else:
            await self.no_game(ctx)


    async def start(self, ctx):
        if ctx.channel.id not in self.current_games: # If no game is currently running in this text channel
            try:
                game = {} # Creating a new dictionary

                with open(const.SCRABBLE_DICTIONARY_PATH, "r", encoding="utf-8") as scrabble_disctionary:
                    game["secret_word"] = random.choice(scrabble_disctionary.readlines()).casefold().strip() # Choosing a secret word in the french lexicon

                game["visible_word"] = "*" * len(game["secret_word"]) # Creating a word with "*" that will be displayed to the players
                game["number_stroke"] = 10 # Players have 10 strokes to find the word
                game["gessed_letters"] = [] # Create the list to store all the guessed letters
                game["definition"] = "Désolé, je n'ai pas trouvé cette définition..." # The definition of the word

                try:
                    async with aiohttp.ClientSession() as session:
                        self.bot.log.warning(f"Asking for word definition")
                        async with session.get(f"https://api.dicolink.com/v1/mot/{game['secret_word']}/definitions?limite=1&api_key={const.DICOLINK_TOKEN}") as r: # Retreve a definition
                            if r.status == 200:
                                definition = await r.json()
                                game["definition"] = definition[0]["definition"]
                except Exception as e:
                    self.bot.log.exception(f"Unable to load a word definition in this channel: {channel.guild}, #{channel.name} ({channel.id})")

                game["starting_time"] = datetime.datetime.now() # We save the datetime of the start of the game

                self.current_games[ctx.channel.id] = game # We add the game dictionary in the class atribute "current_games" linked with the id of the text channel

                response = f"Je lance une partie de pendu !\nVous avez {game['number_stroke']} coup(s) pour trouver le mot secret selon les règles du pendu !\nVoici le mot à deviner : " + game["visible_word"].replace("*", "\*")

            except Exception as e:
                self.bot.log.exception(f"Unable to launch a 'pendu' game in this channel: {channel.guild}, #{channel.name} ({channel.id})")
                response = "Désolé, je n'ai pas réussi à lancer une partie. Veuillez réessayer."

        else: # A game is currently running in this text channel
            response = f"Une partie est déjà en cours !\nIl reste {self.current_games[ctx.channel.id]['number_stroke']} coup(s) et voici le mot à deviner : " + self.current_games[ctx.channel.id]["visible_word"].replace("*", "\*")

        await ctx.send(response)


    async def stop(self, ctx):
        if ctx.channel.id in self.current_games: # If a game is currently running in this text channel
            response = f"Ohhh, dommage, mais je comprend que vous souhaitez arrêter. Voici le mot qui était à deviner : {self.current_games[ctx.channel.id]['secret_word']}"
            del self.current_games[ctx.channel.id]
            await ctx.send(response)
        else: # No game is currently running in this text channel
            await self.no_game(ctx)


    async def no_game(self, ctx):
        response = "Aucune partie de pendu n'est en cours ! Mais vous pouvez en lancer une avec la commande '!pendu start'"
        await ctx.send(response)


    async def restart(self, ctx):
        if ctx.channel.id in self.current_games: # If a game is currently running in this text channel
            response = f"Bon, on recommence. Mais juste pour info, le mot précédent à deviner était : {self.current_games[ctx.channel.id]['secret_word']} ({self.current_games[ctx.channel.id]['definition']})"
            del self.current_games[ctx.channel.id] # Delete the current game
            await ctx.send(response)

        await self.start(ctx)


    async def guess(self, ctx, option):
        if ctx.channel.id in self.current_games: # If a game is currently running in this text channel
            response = ""
            if option in [ re.findall(r"[a-z]", element, flags=re.IGNORECASE)[0] for element in self.current_games[ctx.channel.id]["gessed_letters"] ]: # If the gessed letter has already been guessed
                response = f"Vous avez déjà demandé la lettre {option} !"

            elif option in self.current_games[ctx.channel.id]["secret_word"]: # If the gessed letter is in the secret word
                response = "Oui !"
                self.current_games[ctx.channel.id]["gessed_letters"].append(option) # Add the letter to the gessed letters list

                for i in range(len(self.current_games[ctx.channel.id]["secret_word"])): # Replace the guessed letter in the visible word
                    if self.current_games[ctx.channel.id]["secret_word"][i] == option:
                        self.current_games[ctx.channel.id]["visible_word"] = self.current_games[ctx.channel.id]["visible_word"][:i] + option + self.current_games[ctx.channel.id]["visible_word"][i + 1:]

                if self.current_games[ctx.channel.id]["visible_word"] == self.current_games[ctx.channel.id]["secret_word"]: #WIN
                    response += f" C'est gagné ! Vous avez deviné le mot {self.current_games[ctx.channel.id]['secret_word']} ({self.current_games[ctx.channel.id]['definition']})\nDurée de la partie : {datetime.datetime.now() - self.current_games[ctx.channel.id]['starting_time']}"
                    del self.current_games[ctx.channel.id] # Delete the current game
                    await ctx.send(response)
                    return

            else: # If the guessed letter is not in the secret word
                response = "Non !"
                self.current_games[ctx.channel.id]["gessed_letters"].append(f"~~{option}~~") # Add the letter to the gessed letters list
                self.current_games[ctx.channel.id]["number_stroke"] -= 1 # Decrement the stroke number

                if self.current_games[ctx.channel.id]["number_stroke"] == 0: # LOSE
                    response += " C'est perdu !"
                    response += "\n```\n" + self.hanged_drawing(self.current_games[ctx.channel.id]["number_stroke"]) + "\n```\n"
                    response += f"Le mot à deviner était : {self.current_games[ctx.channel.id]['secret_word']} ({self.current_games[ctx.channel.id]['definition']})"
                    del self.current_games[ctx.channel.id] # Delete the current game
                    await ctx.send(response)
                    return

            await ctx.send(response)
            await self.status(ctx)

        else: # No game is currently running in this text channel
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
            return " ____________\n |/     |\n |      O\n |      |\n |      |\n |\n_|_"
        elif number_stroke == 2:
            return " ____________\n |/     |\n |      O\n |     _|_\n |      |\n |\n_|_"
        elif number_stroke == 1:
            return " ____________\n |/     |\n |      O\n |     _|_\n |      |\n |     /\n_|_"
        elif number_stroke == 0:
            return " ____________\n |/     |\n |      O\n |     _|_\n |      |\n |     / \\ \n_|_"

