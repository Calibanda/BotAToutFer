# quotes command for BotAToutFer
import random

from discord.ext import commands

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="99", help="Responds a B99 quote.")
    async def nine_nine(self, ctx):
        brooklyn_99_quotes = [
            "I'm the human form of the :100: emoji.",
            "Bingpot!",
            "Cool. Cool cool cool cool cool cool cool, no doubt no doubt no doubt no doubt.",
            "Every time someone steps up and says who they are, the world becomes a better, more interesting place.",
            "Haha, angel puked!!",

        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)

    @commands.command(name="good_place", help="Responds a The Good Place quote.")
    async def good_place(self, ctx):
        the_good_place_quotes = [
            "Everything is fine",
            
        ]

        response = random.choice(the_good_place_quotes)
        await ctx.send(response)
