# green command for BotAToutFer
from discord.ext import commands

class Green(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="green", help="Sends a tree.")
    @commands.has_role("Design4green")
    async def green(self, ctx):
        response = ":evergreen_tree:"
        await ctx.send(response)
