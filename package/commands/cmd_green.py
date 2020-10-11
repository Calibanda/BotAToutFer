# green command for BotAToutFer
from discord.ext import commands

class Green(commands.Cog):
    def __init__(self, bot, bot_channel_id):
        self.bot = bot
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="green", help="Envoie un arbre")
    @commands.has_role("Design4green")
    async def green(self, ctx):
        if str(ctx.channel.id) == self.bot_channel_id:
            response = ":evergreen_tree:"
            await ctx.send(response)
