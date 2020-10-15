# siscussion commands for BotAToutFer
import datetime

from discord.ext import commands

class Discussion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="ptdrtki", help="Mec, t'es sérieux ?")
    async def ptdrtki(self, ctx):
        response = f"Alors déjà tu me parle pas comme ça petite :poop:. Ensuite tu sais pas qui je suis ? Sérieux ?\nAlors pour ta culture je suis le grand {self.bot.user.mention}, le bot Discord qui fait tout, même le café !"
        await ctx.send(response)


    @commands.command(name="noel", help="Donne le nombre de jours restants avant Noël")
    async def noel(self, ctx):
        time_delta = datetime.datetime(datetime.datetime.today().year, 12, 25, 0, 0, 0) - datetime.datetime.now()
        if time_delta.days < 0:
            time_delta = datetime.datetime(datetime.datetime.today().year + 1, 12, 25, 0, 0, 0) - datetime.date.now()

        seconds = int(round(time_delta.total_seconds(), 0))
        days = seconds // 86400
        seconds = seconds % 86400

        hours = seconds // 3600
        seconds = seconds % 3600

        minutes = seconds // 60
        seconds = seconds % 60

        response = f"Il reste {days} jour(s), {hours} heure(s), {minutes} minute(s) et {seconds} seconde(s) avant Noël ! :christmas_tree:"
        await ctx.send(response)

        response = f"Un peu de patience {ctx.author.mention}, je sais que tu veux tes cadeaux petit vénal :gift:"
        await ctx.send(response)
