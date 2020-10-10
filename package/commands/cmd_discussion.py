# Discussion commands for BotAToutFer
from discord.ext import commands

class Discussion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="ptdrtki", help="Are you serious?")
    async def ptdrtki(self, ctx):
        response = f"Alors déjà tu me parle pas comme ça petite :poop:. Ensuite tu sais pas qui je suis ? Sérieux ?\nAlors pour ta culture je suis le grand {bot.user.mention}, le bot Discord qui fait tout, même le café !"
        await ctx.send(response)
