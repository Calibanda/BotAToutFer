# drinks command for BotAToutFer
from discord.ext import commands

class Drinks(commands.Cog):
    def __init__(self, bot, bot_channel_id):
        self.bot = bot
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="coffee", help="Send a coffee.")
    async def coffee(self, ctx):
        if str(ctx.channel.id) == self.bot_channel_id:
            response = ":coffee:"
            await ctx.send(response)


    @commands.command(name="tea", help="Send a tea.")
    async def tea(self, ctx):
        if str(ctx.channel.id) == self.bot_channel_id:
            response = ":tea:"
            await ctx.send(response)
