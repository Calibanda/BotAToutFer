# 99 command for BotAToutFer
import random

from discord.ext import commands

class Nine_nine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="99", help="Responds a B99 quote.")
    async def nine_nine(self, ctx):
        brooklyn_99_quotes = [
            "I'm the human form of the :100: emoji.",
            "Bingpot!",
            "Cool. Cool cool cool cool cool cool cool, no doubt no doubt no doubt no doubt.",
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)
