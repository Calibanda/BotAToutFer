# ping command for BotAToutFer
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="ping", help="Répond pong")
    async def ping(self, ctx):
        response = f"pong (latency: {round(self.bot.latency * 1000)}ms)"
        await ctx.send(response)
