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
            "Haha, the angel puked!",
            "- I'm not a thug, I'm police.\n- Ok, then name one law.\n- Don't kill people?\n- It's on me. I set the bar too low...",
            "https://tenor.com/VdlE.gif",
            
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
