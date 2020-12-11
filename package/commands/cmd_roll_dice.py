# roll_dice command for BotAToutFer
import random

from discord.ext import commands

class Roll_dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name="roll", help="Simule un lancer de dés au format xDx")
    async def roll(self, ctx, dice: str=""):
        """Rolls a dice in xDx format."""
        try:
            number_of_dice, number_of_sides = map(int, dice.lower().split('d'))
            if number_of_dice <= 200 and number_of_sides <= 200:
                dices = [ random.randint(1, number_of_sides) for r in range(number_of_dice) ]
                total = sum(dices)
                response = f"**{total}** (" + " + ".join(str(d) for d in dices) + f" = {total})"
            else:
                response = "Ohh la flemme de lancer tous ces dés !"
            
            await ctx.send(response)
        except Exception:
            await ctx.send('Format has to be in xDx!')
