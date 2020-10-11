# quotes command for BotAToutFer
import random

from discord.ext import commands

class Quotes(commands.Cog):
    def __init__(self, bot, bot_channel_id):
        self.bot = bot
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="99", help="Répond une réplique de B99")
    async def nine_nine(self, ctx):
        if str(ctx.channel.id) == self.bot_channel_id:
            brooklyn_99_quotes = [
                "I'm the human form of the :100: emoji.",
                "Bingpot!",
                "Cool. Cool cool cool cool cool cool cool, no doubt no doubt no doubt no doubt.",
                "Every time someone steps up and says who they are, the world becomes a better, more interesting place.",
                "Haha, the angel puked!",
                "- I'm not a thug, I'm police.\n- Ok, then name one law.\n- Don't kill people?\n- It's on me. I set the bar too low...",
                "https://tenor.com/VdlE.gif",
                "YOU PUNK!",
                
            ]

            response = random.choice(brooklyn_99_quotes)
            await ctx.send(response)

    @commands.command(name="good_place", help="Répond une réplique de TGP")
    async def good_place(self, ctx):
        if str(ctx.channel.id) == self.bot_channel_id:
            the_good_place_quotes = [
                "Everything is fine",
                "I'm telling you, Molotov cocktails work. Anytime I had a problem and I threw a Molotov cocktail, boom! Right away, I had a different problem.",
                "Not a girl",
                
            ]

            response = random.choice(the_good_place_quotes)
            await ctx.send(response)
