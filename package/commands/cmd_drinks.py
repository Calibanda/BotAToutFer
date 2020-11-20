# drinks command for BotAToutFer
import aiohttp

from discord.ext import commands

import const

class Drinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name="coffee", help="Envoie un café")
    @commands.has_role("CoffeeMaker")
    async def coffee(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(const.COFFEE_URL, params={'token': const.COFFEE_TOKEN}) as r:
                if r.status == 200:
                    response = "Je lance le café :coffee:"
                else:
                    response = "Ah, non, pas de café :cry:"
                await ctx.send(response)


    @commands.command(name="tea", help="Envoie un thé")
    async def tea(self, ctx):
        response = ":tea:"
        await ctx.send(response)
