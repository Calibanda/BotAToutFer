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
        self.CURSE_LIST = [ # The list of cursed words
            {"curse_word": "merde", "traduction": "merle"},
            {"curse_word": "putain", "traduction": "mutin"},
            {"curse_word": "connard", "traduction": "canard"},
            {"curse_word": "connarde", "traduction": "canarde"},
            {"curse_word": "connasse", "traduction": "godasse"},
            {"curse_word": "pute", "traduction": "butte"},
            {"curse_word": "bordel", "traduction": "bordé"},
            {"curse_word": "foutre", "traduction": "floute"},
            #{"curse_word": "poufiace", "traduction": ""},
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

        self.DICO_MARSEILLAIS_PATH = os.path.join(self.bot.SCRIPT_DIR, "package", "dico_marseillais.json")

        try:
            with open(self.DICO_MARSEILLAIS_PATH, "r") as f:
                self.DICO_MARSEILLAIS = json.load(f)
        except Exception as e:
            self.bot.log.error(f"Catched exeption:", exc_info=e)
            self.DICO_MARSEILLAIS = []


    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        if message.author == self.bot.user:
            # await self.bot.process_commands(message)
            return
        else: # This doesn't invoke a command!
            words_in_message = [ word for word in re.split("\W", message.content.lower()) if word ] # We split the words in the message on any non word character (\W) and ignore empty words

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


    async def joke_je_suis(self, message):
        if any(je_suis in message.content.lower() for je_suis in self.LIST_JE_SUIS):
            regex_je_suis = "(" + ")|(".join(self.LIST_JE_SUIS) + ")" # "(je suis)|(j'suis)|(chuis) ..."
            i_am = re.split(regex_je_suis, message.content, 1, flags=re.IGNORECASE)[-1]
            response = f"Salut *{i_am}*, moi c'est le {self.bot.user.mention}"
            await message.channel.send(response)


    async def joke_echec(self, message, words_in_message):
        if [ word for word in words_in_message if word in {"échec", "echec"} ]: # If common words between words in the original message and "échec" or "echec"
            response = "https://tenor.com/bq4o5.gif"
            await message.channel.send(response)


    async def joke_possible(self, message, words_in_message):
        if [ word for word in words_in_message if word in {"possible", "impossible"} ]: # If common words between words in the original message and "possible" or "impossible"
            response = "https://tenor.com/XiKZ.gif"
            await message.channel.send(response)


    async def joke_aled(self, message, words_in_message):
        if "aled" in words_in_message: # If the word "aled" in the original message
            response ="https://assets.classicfm.com/2017/23/aled-jones-new-1497019550-editorial-long-form-1.png"
            await message.channel.send(response)


    async def mousse(self, message, words_in_message):
        if "attention" in words_in_message or "mousse" in words_in_message: # If the words "attention" or "mousse" in the original message
            response ="https://media1.tenor.com/images/ef6a3c5ba7cbdc4b0140d7363dbc841f/tenor.gif" # Send the "ATTENTION À LA MOUSSE !!" gif
            await message.channel.send(response)


    async def projet(self, message, words_in_message):
        if "projet" in words_in_message: # If the words "projet" in the original message
            response ="https://tenor.com/RGiO.gif" # Send the "CAR C'EST NOTRE PROJEEEEET !!" gif
            await message.channel.send(response)


    async def cursed_words(self, message, words_in_message):
        if [ word for word in words_in_message for curse_dict in self.CURSE_LIST if word == curse_dict["curse_word"] ]: # If any curse word in the original message
            response = message.content
            for curse_dict in self.CURSE_LIST:
                response = re.sub(r"(?<!\:)" + curse_dict["curse_word"], "*" + curse_dict["traduction"] + "*", response, 0, flags=re.IGNORECASE)

            response = f"{message.author.mention} : {response}"
            await message.channel.send(response)
            await message.delete()


    async def respect(self, message, words_in_message):
        if "respecter" in words_in_message or "respecte" in words_in_message: # If the words "respecter" or "respecte" in the original message
            response ="https://tenor.com/view/master-spongebob-bowing-bow-yes-master-gif-5594685" # Send the "Yes master" gif
            await message.channel.send(response)


    async def what(self, message, words_in_message):
        if "what" in words_in_message: # If the word "what" in the original message
            response ="https://tenor.com/view/minion-what-huh-gif-9361819" # Send a "WHHAAAATTT?!" minion gif
            await message.channel.send(response)


    async def rip(self, message, words_in_message):
        if "rip" in words_in_message: # If the word "rip" in the original message
            response ="https://tenor.com/view/rip-coffin-black-ghana-celebrating-gif-16743302" # Send a "RIP" minion gif
            await message.channel.send(response)
