# roll_dice command for BotAToutFer
import random

from discord.ext import commands

class Roll_dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="roll_dice", help="Simulates rolling dice.")
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [ str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice) ]
        response = ", ".join(dice)
        await ctx.send(response)
