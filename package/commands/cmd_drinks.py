# drinks command for BotAToutFer
from discord.ext import commands

class Drinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="coffee", help="Send a coffee.")
    async def coffee(self, ctx):
        response = ":coffee:"
        await ctx.send(response)


    @commands.command(name="tea", help="Send a tea.")
    async def tea(self, ctx):
        response = ":tea:"
        await ctx.send(response)
