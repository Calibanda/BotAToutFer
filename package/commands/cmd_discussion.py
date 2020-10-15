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

        #number_days = time_delta.days
        #number_hours = time_delta.seconds - number_days // 3600
        #number_minutes = time_delta - number_days - number_hours // 60

        response = f"Il reste {time_delta.days} jour(s), avant Noël ! :christmas_tree:"
        await ctx.send(response)
