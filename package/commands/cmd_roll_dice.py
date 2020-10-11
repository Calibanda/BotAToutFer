# roll_dice command for BotAToutFer
import random

from discord.ext import commands

class Roll_dice(commands.Cog):
    def __init__(self, bot, bot_channel_id):
        self.bot = bot
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="roll_dice", help="Simule un lancer de dés au format xDx")
    async def roll(self, ctx, dice: str):
        """Rolls a dice in xDx format."""
        if str(ctx.channel.id) == self.bot_channel_id:
            try:
                number_of_sides, number_of_dice = map(int, dice.lower().split('d'))
                response = ", ".join(str(random.randint(1, number_of_sides)) for r in range(number_of_dice))
                await ctx.send(response)
            except Exception:
                await ctx.send('Format has to be in xDx!')
