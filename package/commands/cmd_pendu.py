# hanged commands for BotAToutFer
import os
import random
import json
import re

from discord.ext import commands

import const

class Pendu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        self.playing = False
        self.secret_word = ""
        self.visible_word = ""
        self.number_stroke = 10
        self.gessed_letters = []
    
    @commands.command(name="pendu", help="Joue au pendu")
    async def pendu(self, ctx, option: str="help"):
        option = option.casefold().strip()

        if option=="status":
            await self.display_status_message(ctx)

        elif option=="start" and not self.playing:
            await self.start(ctx)

        elif option=="start":
            response = f"Une partie est déjà en cours !\nIl reste {self.number_stroke} coup(s) et voici le mot à deviner : " + self.visible_word.replace("*", "\*")
            await ctx.send(response)

        elif option=="stop" and not self.playing:
            response = "Aucune partie de pendu n'est en cours ! Mais vous pouvez en lancer une avec la commande '!pendu start'"
            await ctx.send(response)

        elif option=="stop":
            self.playing = False
            response = f"Ohhh, dommage, mais je comprend que vous souhaitez arrêter. Voici le mot qui était à deviner : {self.secret_word}"
            await ctx.send(response)

        elif option=="restart" or option=="reboot":
            if self.playing:
                response = f"Bon, on recommence. Mais juste pour info, le mot précédent à deviner était : {self.secret_word}"
                await ctx.send(response)

            await self.start(ctx)

        elif re.match(r"^[a-z]$", option):
            response = ""
            if option in self.gessed_letters:
                response = f"Vous avez déjà demandé la lettre {option} !"

            elif option in self.secret_word:
                response = "Oui !"
                self.gessed_letters.append(option)

                for i in range(len(self.secret_word)):
                    if self.secret_word[i] == option:
                        self.visible_word = self.visible_word[:i] + option + self.visible_word[i + 1:]
                if self.visible_word == self.secret_word: #WIN
                    response += f" C'est gagné ! Vous avez deviné le mot {self.secret_word}."
                    await ctx.send(response)
                    return

            else:
                response = "Non !"
                self.gessed_letters.append(f"~~{option}~~")
                self.number_stroke -= 1

                if self.number_stroke == 0: # LOSE
                    response += " C'est perdu !"
                    self.playing = False
                    response += "\n```\n" + self.hanged_drawing() + "\n```\n"
                    response += f"Le mot à deviner était : {self.secret_word}"
                    await ctx.send(response)
                    return

            await ctx.send(response)
            await self.display_status_message(ctx)

        else: # Display help
            response = "Les commandes du jeu du pendu :\n```\n!pendu start                       Lance une partie\n!pendu stop                        Arrête la partie en cours\n!pendu restart (ou !pendu reboot)  Arrête la partie en cours et en relance une\n!pendu status                      Affiche le status de la partie en cours\n!pendu <lettre>                    Proposer une lettre\n```"
            await ctx.send(response)


    async def start(self, ctx):
        self.playing = True
        self.number_stroke = 10
        self.gessed_letters = []
        with open(const.SCRABBLE_DICTIONARY_PATH, "r", encoding="utf-8") as scrabble_disctionary:
            self.secret_word = random.choice(scrabble_disctionary.readlines()).casefold().strip()

        self.visible_word = "*" * len(self.secret_word)

        response = f"Je lance une partie de pendu !\nVous avez {self.number_stroke} coup(s) pour trouver le mot secret selon les règles du pendu !\nVoici le mot à deviner : " + self.visible_word.replace("*", "\*")
        await ctx.send(response)


    def hanged_drawing(self):
        if self.number_stroke == 10:
            return ""
        elif self.number_stroke == 9:
            return "___"
        elif self.number_stroke == 8:
            return " |\n |\n |\n |\n |\n_|_"
        elif self.number_stroke == 7:
            return " ____________\n |\n |\n |\n |\n |\n_|_"
        elif self.number_stroke == 6:
            return " ____________\n |/\n |\n |\n |\n |\n_|_"
        elif self.number_stroke == 5:
            return " ____________\n |/     |\n |\n |\n |\n |\n_|_"
        elif self.number_stroke == 4:
            return " ____________\n |/     |\n |      O\n |\n |\n |\n_|_"
        elif self.number_stroke == 3:
            return " ____________\n |/     |\n |      O\n |      |\n |      |\n |\n_|_"
        elif self.number_stroke == 2:
            return " ____________\n |/     |\n |      O\n |     _|_\n |      |\n |\n_|_"
        elif self.number_stroke == 1:
            return " ____________\n |/     |\n |      O\n |     _|_\n |      |\n |     /\n_|_"
        elif self.number_stroke == 0:
            return " ____________\n |/     |\n |      O\n |     _|_\n |      |\n |     / \\ \n_|_"


    async def display_status_message(self, ctx):
        if self.playing:
            response = "Le mot à deviner : " + self.visible_word.replace("*", "\*") + "\nLes lettres déjà proposées : "
            for letter in self.gessed_letters:
                response += f"{letter} "
            response += "\nLe pendu :\n```\n" + self.hanged_drawing() + "\n```"
        else:
            response = "Aucune partie en cours !"
        await ctx.send(response)
