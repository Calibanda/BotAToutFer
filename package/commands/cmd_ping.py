# ping command for BotAToutFer
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot, bot_channel_id):
        self.bot = bot
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="ping", help="Répond pong")
    async def ping(self, ctx):
        if str(ctx.channel.id) == self.bot_channel_id:
            response = "pong"
            await ctx.send(response)
