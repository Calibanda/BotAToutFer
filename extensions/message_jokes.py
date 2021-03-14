# jokes on messages for BotÀToutFer
import os
import json
import re

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Jokes(bot))


class Jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.hidden_cog = True
        self.LIST_JE_SUIS = [
            "je suis ",
            "j'suis ",
            "chuis ",
            "chui ",
            "j'sui ",
            "j suis ",
            "j sui ",
        ]
        self.CURSE_LIST = [  # The list of cursed words
            {"curse_word": "merde", "traduction": "merle"},
            {"curse_word": "putain", "traduction": "mutin"},
            {"curse_word": "connard", "traduction": "canard"},
            {"curse_word": "connarde", "traduction": "canarde"},
            {"curse_word": "connasse", "traduction": "godasse"},
            {"curse_word": "pute", "traduction": "butte"},
            {"curse_word": "bordel", "traduction": "bordé"},
            {"curse_word": "foutre", "traduction": "floute"},
            # {"curse_word": "poufiace", "traduction": ""},
            {"curse_word": "enculé", "traduction": "granulé"},

            {"curse_word": "fuck", "traduction": "fork"},
            {"curse_word": "fucking", "traduction": "forking"},
            {"curse_word": "fucker", "traduction": "forker"},
            {"curse_word": "shit", "traduction": "shirt"},
            {"curse_word": "bitch", "traduction": "bench"},
            {"curse_word": "asshole", "traduction": "ash-hole"},
            {"curse_word": "ass", "traduction": "ash"},
            {"curse_word": "cock", "traduction": "cork"},
            {"curse_word": "dick", "traduction": "deck"},
        ]

    @commands.Cog.listener('on_message')
    async def message_jokes(self, message):
        if message.author == self.bot.user:
            return

        words_in_message = []
        for word in re.split("\W", message.content.lower()):
            # We split the words in the message
            # on any non word character (\W)
            if word:
                # We ignore empty words
                words_in_message.append(word)

        await self.joke_je_suis(message)
        await self.joke_echec(message, words_in_message)
        await self.joke_possible(message, words_in_message)
        await self.joke_aled(message, words_in_message)
        await self.cursed_words(message, words_in_message)
        await self.mousse(message, words_in_message)
        await self.projet(message, words_in_message)
        await self.respect(message, words_in_message)
        await self.what(message, words_in_message)
        await self.rip(message, words_in_message)
        await self.alerte(message, words_in_message)

    async def joke_je_suis(self, message):
        has_suis = False
        for je_suis in self.LIST_JE_SUIS:
            if je_suis in message.content.lower():
                has_suis = True

        if has_suis:
            # If any "je suis" in the original message
            regex_je_suis = (  # "(je suis)|(j'suis)|(chuis) ..."
                "("
                + ")|(".join(self.LIST_JE_SUIS)
                + ")"
            )
            i_am = re.split(
                regex_je_suis,
                message.content,
                1,
                flags=re.IGNORECASE
            )[-1]
            response = f"Salut *{i_am}*, moi c'est le {self.bot.user.mention}"
            await message.channel.send(response)

    async def joke_echec(self, message, words_in_message):
        if "échec" in words_in_message or "echec" in words_in_message:
            # If the words "échec" or "echec" in the original message
            response = "https://tenor.com/bq4o5.gif"
            await message.channel.send(response)

    async def joke_possible(self, message, words_in_message):
        if "possible" in words_in_message or "impossible" in words_in_message:
            # If the words "possible" or "impossible" in the original message
            response = "https://tenor.com/XiKZ.gif"
            await message.channel.send(response)

    async def joke_aled(self, message, words_in_message):
        if "aled" in words_in_message:
            # If the word "aled" in the original message
            response = (
                "https://assets.classicfm.com/2017/23/aled-jones-new-"
                + "1497019550-editorial-long-form-1.png"
            )
            await message.channel.send(response)

    async def cursed_words(self, message, words_in_message):
        has_curse_word = False
        for word in words_in_message:
            for curse_dict in self.CURSE_LIST:
                if word == curse_dict["curse_word"]:
                    has_curse_word = True

        if has_curse_word:
            # If any curse word in the original message
            response = message.content
            for curse_dict in self.CURSE_LIST:
                response = re.sub(
                    r"(?<!\:)" + curse_dict["curse_word"],
                    "*" + curse_dict["traduction"] + "*",
                    response,
                    0,
                    flags=re.IGNORECASE
                )

            response = f"{message.author.mention} : {response}"
            await message.channel.send(response)
            await message.delete()

    async def mousse(self, message, words_in_message):
        if "attention" in words_in_message or "mousse" in words_in_message:
            # If the words "attention" or "mousse" in the original message
            response = (  # Send the "ATTENTION À LA MOUSSE !!" gif
                "https://media1.tenor.com/images/"
                + "ef6a3c5ba7cbdc4b0140d7363dbc841f/tenor.gif"
            )
            await message.channel.send(response)

    async def projet(self, message, words_in_message):
        if "projet" in words_in_message:
            # If the words "projet" in the original message
            response = "https://tenor.com/RGiO.gif"
            # Send the "CAR C'EST NOTRE PROJEEEEET !!" gif
            await message.channel.send(response)

    async def respect(self, message, words_in_message):
        if "respecter" in words_in_message or "respecte" in words_in_message:
            # If the words "respecter" or "respecte" in the original message
            response = (  # Send the "Yes master" gif
                "https://tenor.com/view/master-spongebob-bowing-bow-yes-"
                + "master-gif-5594685"
            )
            await message.channel.send(response)

    async def what(self, message, words_in_message):
        if "what" in words_in_message:
            # If the word "what" in the original message
            response = (  # Send a "WHHAAAATTT?!" minion gif
                "https://tenor.com/view/minion-what-huh-gif-9361819"
            )
            await message.channel.send(response)

    async def rip(self, message, words_in_message):
        if "rip" in words_in_message:
            # If the word "rip" in the original message
            response = (  # Send a "RIP" gif
                "https://tenor.com/view/rip-coffin-black-ghana-"
                + "celebrating-gif-16743302"
            )
            await message.channel.send(response)

    async def alerte(self, message, words_in_message):
        if "alerte" in words_in_message:
            # If the word "alerte" in the original message
            response = (  # Send a "ALERTE GÉNÉRALE !" gif
                "https://tenor.com/view/shout-yell-alerte-generale-alert-"
                + "alerted-general-gif-17332933"
            )
            await message.channel.send(response)
