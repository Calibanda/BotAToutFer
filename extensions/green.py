# green command for BotÀToutFer
from discord.ext import commands


def setup(bot):
    bot.add_cog(Green(bot))


class Green(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="green", help="Envoie un arbre")
    @commands.has_role("Design4green")
    async def green(self, ctx):
        response = ":evergreen_tree:"
        await ctx.send(response)
