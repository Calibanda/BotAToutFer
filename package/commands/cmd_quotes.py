# quotes command for BotAToutFer
import secrets

from discord.ext import commands

import const

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="99", help="Répond une réplique de B99")
    async def nine_nine(self, ctx):
        response = secrets.choice(const.brooklyn_99_quotes)
        await ctx.send(response)

    @commands.command(name="good_place", help="Répond une réplique de TGP")
    async def good_place(self, ctx):
        response = secrets.choice(const.the_good_place_quotes)
        await ctx.send(response)

    @commands.command(name="sherlock", help="Répond une réplique de Sherlock")
    async def sherlock(self, ctx):
        response = secrets.choice(const.sherlock_quotes)
        await ctx.send(response)

    @commands.command(name="kaamelott", help="Répond une réplique de Kaamelott")
    async def kaamelott(self, ctx):
        response = secrets.choice(const.kaamelott_quotes)
        if len(response) < 2000:
            await ctx.send(response)
        else:
            for subresponse in response.split("\n"):
                await ctx.send(subresponse)
