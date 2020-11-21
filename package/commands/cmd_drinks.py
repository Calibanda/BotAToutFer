# drinks command for BotAToutFer
import urllib3

from discord.ext import commands

import const

class Drinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name="coffee", help="Envoie un café")
    @commands.has_role("CoffeeMaker")
    async def coffee(self, ctx):
        http = urllib3.PoolManager()
        #http_response = http.request("GET", const.COFFEE_URL)
        #http_response = http.request("POST", const.COFFEE_URL, fields={"token": const.COFFEE_TOKEN})
        http_response = http.request("BREW", const.COFFEE_URL, fields={"token": const.COFFEE_TOKEN}, headers={"Accept-Additions": "sweetener-type"})
        if http_response.status == 200:
            response = "Je lance le café :coffee:"
        else:
            response = "Ah, non, pas de café :cry:"
        await ctx.send(response)


    @commands.command(name="tea", help="Envoie un thé")
    async def tea(self, ctx):
        response = ":tea:"
        await ctx.send(response)
