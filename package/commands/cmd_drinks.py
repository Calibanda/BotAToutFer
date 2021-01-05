# drinks commands for BotAToutFer
import urllib3

from discord.ext import commands

import const

class Drinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name="coffee-start", help="Lance le café")
    @commands.has_role("CoffeeMaker")
    async def coffee_start(self, ctx):
        http = urllib3.PoolManager(retries=False, timeout=5.0)

        try:
            http_response = http.request("BREW", const.COFFEE_URL, fields={"passwd": const.COFFEE_PASSWORD, "action": "start"})
            #http_response = http.request("BREW", const.COFFEE_URL, fields={"passwd": const.COFFEE_PASSWORD, "action": "start"}, headers={"Accept-Additions": "sweetener-type"})
            if http_response.status == 200:
                response = "Je lance le café :coffee:"
            else:
                response = "Ah, non, pas de café :cry:"
        except Exception as e:
            self.bot.log.exception(f"Unable to order a coffee: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})")
            response = "https://tenor.com/view/still-waiting-for-reply-waiting-patience-bored-hurry-up-gif-10179642"

        await ctx.send(response)


    @commands.command(name="coffee-stop", help="Stope le café")
    @commands.has_role("CoffeeMaker")
    async def coffee_stop(self, ctx):
        http = urllib3.PoolManager(retries=False, timeout=5.0)

        try:
            http_response = http.request("BREW", const.COFFEE_URL, fields={"passwd": const.COFFEE_PASSWORD, "action": "stop"})
            #http_response = http.request("BREW", const.COFFEE_URL, fields={"passwd": const.COFFEE_PASSWORD, "action": "stop"}, headers={"Accept-Additions": "sweetener-type"})
            if http_response.status == 200:
                response = "Je stope le café :coffee:"
            else:
                response = "Ah, non, pas de café :cry:"
        except Exception as e:
            self.bot.log.exception(f"Unable to stop the coffee: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})")
            response = "https://tenor.com/view/still-waiting-for-reply-waiting-patience-bored-hurry-up-gif-10179642"

        await ctx.send(response)


    @commands.command(name="coffee-when", help="Affiche depuis combien de temps le café a été lancé")
    @commands.has_role("CoffeeMaker")
    async def coffee_when(self, ctx):
        http = urllib3.PoolManager(retries=False, timeout=5.0)

        try:
            http_response = http.request("WHEN", const.COFFEE_URL)
            time = int(http_response.data)
            if time > 0:
                response = f"Un café est lancé depuis {time}"
            else:
                response = "Pas de café en cours !"
        except Exception as e:
            self.bot.log.exception(f"Unable to stop the coffee: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})")
            response = "https://tenor.com/view/still-waiting-for-reply-waiting-patience-bored-hurry-up-gif-10179642"

        await ctx.send(response)


    @commands.command(name="tea", help="Envoie un thé")
    async def tea(self, ctx):
        response = ":tea:"
        await ctx.send(response)
