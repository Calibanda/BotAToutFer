# siscussion commands for BotAToutFer
from discord.ext import commands

class Discussion(commands.Cog):
    def __init__(self, bot, bot_channel_id):
        self.bot = bot
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="ptdrtki", help="Mec, t'es sérieux ?")
    async def ptdrtki(self, ctx):
        if str(ctx.channel.id) == self.bot_channel_id:
            response = f"Alors déjà tu me parle pas comme ça petite :poop:. Ensuite tu sais pas qui je suis ? Sérieux ?\nAlors pour ta culture je suis le grand {self.bot.user.mention}, le bot Discord qui fait tout, même le café !"
            await ctx.send(response)
