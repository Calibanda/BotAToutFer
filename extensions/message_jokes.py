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

        self.CURSE_DICT = {  # The dictionary of cursed words
            "merde": "merle",
            "putain": "mutin",
            "connard": "canard",
            "connarde": "canarde",
            "connasse": "godasse",
            "pute": "butte",
            "bordel": "bordé",
            "foutre": "floute",
            # "poufiace": "",
            "enculé": "granulé",

            "fuck": "fork",
            "fucking": "forking",
            "fucker": "forker",
            "shit": "shirt",
            "bitch": "bench",
            "asshole": "ash-hole",
            "ass": "ash",
            "cock": "cork",
            "dick": "deck",
        }

        self.JOKE_WORDS_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "joke_words.json"
        )

        try:
            with open(self.JOKE_WORDS_PATH, "r") as f:
                self.joke_words = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error("joke_words.json file not found: ", exc_info=e)
            self.joke_words = {}

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
        await self.cursed_words(message, words_in_message)

        for key, value in self.joke_words.items():
            if key in words_in_message:
                await message.channel.send(value)

    async def joke_je_suis(self, message):
        has_suis = False
        for je_suis in self.LIST_JE_SUIS:
            if je_suis in message.content.lower():
                has_suis = True

        if has_suis:
            # If any "je suis" in the original message
            regex_je_suis = "(" + ")|(".join(self.LIST_JE_SUIS) + ")"  # "(je suis)|(j'suis)|(chuis) ..."
            i_am = re.split(
                pattern=regex_je_suis,
                string=message.content,
                maxsplit=1,
                flags=re.IGNORECASE
            )[-1]
            response = f"Salut *{i_am}*, moi c'est le {self.bot.user.mention}"
            await message.channel.send(response)

    async def cursed_words(self, message, words_in_message):
        has_curse_word = False
        for word in words_in_message:
            if word in self.CURSE_DICT:
                has_curse_word = True

        if has_curse_word:
            # If any curse word in the original message
            response = message.content
            for curse_word, traduction in self.CURSE_DICT.items():
                response = re.sub(
                    pattern=r"(?<!\:)" + curse_word,
                    repl=f"*{traduction}*",
                    string=response,
                    count=0,
                    flags=re.IGNORECASE
                )

            response = f"{message.author.mention} : {response}"
            await message.channel.send(response)
            await message.delete()

    @commands.command(name="add-joke")
    @commands.is_owner()
    async def add_joke(self, ctx, trigger_word, gif_url):
        self.joke_words[trigger_word] = gif_url
        with open(self.JOKE_WORDS_PATH, "w", encoding="utf8") as f:
            json.dump(self.joke_words, f, indent=4, ensure_ascii=False)

        await ctx.send(gif_url)

    @commands.command(name="remove-joke")
    @commands.is_owner()
    async def remove_joke(self, ctx, trigger_word):
        try:
            del self.joke_words[trigger_word]
        except KeyError as e:
            await ctx.send("This trigger word does not exist !")
        else:
            with open(self.JOKE_WORDS_PATH, "w", encoding="utf8") as f:
                json.dump(self.joke_words, f, indent=4, ensure_ascii=False)
            await ctx.send(f"{trigger_word} deleted.")
