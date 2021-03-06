# drinks commands for BotÀToutFer
import urllib3

from discord.ext import commands


def setup(bot):
    bot.add_cog(Drinks(bot))


class Drinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.http = urllib3.PoolManager(retries=False, timeout=20.0)

    @commands.command(name="coffee-start", help="Lance le café")
    @commands.has_role("CoffeeMaker")
    async def coffee_start(self, ctx):
        try:
            http_response = self.http.request(
                method="BREW",
                url=self.bot.COFFEE_URL,
                fields={"passwd": self.bot.COFFEE_PASSWORD, "action": "start"}
            )
            if http_response.status == 200:
                response = "Je lance le café :coffee:"
            else:
                response = "Ah, non, pas de café :cry:"
        except urllib3.exceptions.TimeoutError as e:
            self.bot.log.exception(f"HTCPCP timeout: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            response = "https://tenor.com/view/still-waiting-for-reply-waiting-patience-bored-hurry-up-gif-10179642"

        except Exception as e:
            self.bot.log.exception(f"An exception occurred during HTCPCP START :{ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            response = "Une erreur inconnue est apparue"

        await ctx.send(response)

    @commands.command(name="coffee-stop", help="Stope le café")
    @commands.has_role("CoffeeMaker")
    async def coffee_stop(self, ctx):
        try:
            http_response = self.http.request(
                method="BREW",
                url=self.bot.COFFEE_URL,
                fields={"passwd": self.bot.COFFEE_PASSWORD, "action": "stop"}
            )
            if http_response.status == 200:
                response = "Je stope le café :coffee:"
            else:
                response = "Ah, non, pas de café :cry:"
        except urllib3.exceptions.TimeoutError as e:
            self.bot.log.exception(f"HTCPCP timeout: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            response = "https://tenor.com/view/still-waiting-for-reply-waiting-patience-bored-hurry-up-gif-10179642"

        except Exception as e:
            self.bot.log.exception(f"An exception occurred during HTCPCP STOP : {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            response = "Une erreur inconnue est apparue"

        await ctx.send(response)

    @commands.command(name="coffee-when", help="Affiche depuis combien de temps le café a été lancé")
    @commands.has_role("CoffeeMaker")
    async def coffee_when(self, ctx):
        try:
            http_response = self.http.request(
                method="WHEN",
                url=self.bot.COFFEE_URL
            )
            time = float(http_response.data)
            if time > 0:
                response = f"Un café est lancé depuis {round(time / 1000, 2)} secondes"
            else:
                response = "Pas de café en cours !"
        except urllib3.exceptions.TimeoutError as e:
            self.bot.log.exception(f"HTCPCP timeout: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            response = "https://tenor.com/view/still-waiting-for-reply-waiting-patience-bored-hurry-up-gif-10179642"

        except Exception as e:
            self.bot.log.exception(f"An exception occured during HTCPCP WHEN : {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            response = "Une erreur inconnue est apparue"

        await ctx.send(response)

    @commands.command(name="tea", help="Envoie un thé")
    async def tea(self, ctx):
        response = ":tea:"
        await ctx.send(response)
