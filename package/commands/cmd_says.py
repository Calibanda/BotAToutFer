# says command for BotAToutFer
from discord.ext import commands

class Says(commands.Cog):
    def __init__(self, bot, bot_channel_id):
        self.bot = bot
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="says", help="Make the bot says something.")
    async def says(self, ctx, *, arg: str):
        if str(ctx.channel.id) == self.bot_channel_id:
            response = arg
            await ctx.message.delete()
            await ctx.send(response)
