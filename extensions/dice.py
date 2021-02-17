# dice commands for BotÀToutFer
import random

from discord.ext import commands


def setup(bot):
    bot.add_cog(Roll_dice(bot))


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
        except Exception as e:
            self.bot.log.error(f"Catched exeption:", exc_info=e)
            await ctx.send('Format has to be in xDx!')


    @commands.command(name="roll-sw", help="Simule un lancer de dés Star Wars au format xD<name>")
    async def roll_sw(self, ctx, dice: str=""):
        """Rolls a dice in xD<name> format."""
        try:
            number_of_dice, dice_type = dice.lower().split('d', maxsplit=1)
            number_of_dice = int(number_of_dice)
            if number_of_dice > 200:
                response = "Ohh la flemme de lancer tous ces dés !"
            else:
                if dice_type == "fortune" or dice_type == "f":
                    sides = [
                        "Vierge :shrug:",
                        "Vierge :shrug:",
                        "Succès net :boom:",
                        "Succès net :boom: et Avantage :trident:",
                        "Avantage :trident:",
                        "2 Avantages :trident: :trident:"
                    ]
                elif dice_type == "infortune" or dice_type == "i":
                    sides = [
                        "Vierge :shrug:",
                        "Échec :warning:",
                        "Menace :snowflake:"
                    ]
                elif dice_type == "aptitude" or dice_type == "a":
                    sides = [
                        "Vierge :shrug:",
                        "Succès net :boom:",
                        "Succès net :boom:",
                        "2 Succès net :boom: :boom:",
                        "Succès net :boom: et Avantage :trident:",
                        "Avantage :trident:",
                        "Avantage :trident:",
                        "2 Avantages :trident: :trident:"
                    ]
                elif dice_type == "difficulte" or dice_type == "difficulté" or dice_type == "d":
                    sides = [
                        "Vierge :shrug:",
                        "Échec :warning:",
                        "2 Échecs :warning: :warning:",
                        "Échec :warning: et Menace :snowflake:",
                        "Menace :snowflake:",
                        "Menace :snowflake:",
                        "Menace :snowflake:",
                        "2 Menaces :snowflake: :snowflake:"
                    ]
                elif dice_type == "maitrise" or dice_type == "maîtrise" or dice_type == "m":
                    sides = [
                        "Vierge :shrug:",
                        "Succès net :boom:",
                        "Succès net :boom:",
                        "2 Succès net :boom: :boom:",
                        "2 Succès net :boom: :boom:",
                        "Succès net :boom: et Avantage :trident:",
                        "Succès net :boom: et Avantage :trident:",
                        "Succès net :boom: et Avantage :trident:",
                        "Avantage :trident:",
                        "2 Avantages :trident: :trident:",
                        "2 Avantages :trident: :trident:",
                        "Triomphe :tada:"
                    ]
                elif dice_type == "defi" or dice_type == "défi":
                    sides = [
                        "Vierge :shrug:",
                        "Échec :warning:",
                        "Échec :warning:",
                        "2 Échecs :warning: :warning:",
                        "2 Échecs :warning: :warning:",
                        "Échec :warning: et Menace :snowflake:",
                        "Échec :warning: et Menace :snowflake:",
                        "Menace :snowflake:",
                        "Menace :snowflake:",
                        "2 Menaces :snowflake: :snowflake:",
                        "2 Menaces :snowflake: :snowflake:",
                        "Désatre :rotating_light:"
                    ]
                elif dice_type == "force":
                    sides = [
                        "Côté obscur :black_circle:",
                        "Côté obscur :black_circle:",
                        "Côté obscur :black_circle:",
                        "Côté obscur :black_circle:",
                        "Côté obscur :black_circle:",
                        "Côté obscur :black_circle:",
                        "2 Côté obscur :black_circle: :black_circle:",
                        "Côté lumineux :white_circle:",
                        "Côté lumineux :white_circle:",
                        "2 Côté lumineux :white_circle: :white_circle:",
                        "2 Côté lumineux :white_circle: :white_circle:",
                        "2 Côté lumineux :white_circle: :white_circle:",
                    ]
                else:
                    response = "Merci de choisir un dé parmi : fortune (ou f), infortune (ou i), aptitude (ou a), difficulte (ou d), maitrise (ou m), defi, force"
                    await ctx.send(response)
                    return

                dices = [ random.choice(sides) for r in range(number_of_dice) ]
                response = " + ".join(str(d) for d in dices)

            await ctx.send(response)
        except Exception as e:
            self.bot.log.error(f"Catched exeption:", exc_info=e)
            await ctx.send('Format has to be in xD<name>!')
