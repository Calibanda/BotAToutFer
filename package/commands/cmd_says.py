# says command for BotAToutFer
from discord.ext import commands

class Says(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="says", help="Fait dire quelque chose au bot")
    async def says(self, ctx, *, arg: str):
        response = arg
        await ctx.message.delete()
        await ctx.send(response)
