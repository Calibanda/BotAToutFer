# dice commands for BotÀToutFer
import secrets
import re
import ast
import operator as op

from discord.ext import commands


def setup(bot):
    bot.add_cog(RollDice(bot))


class RollDice(commands.Cog, name="Jets de dés"):
    def __init__(self, bot):
        self.bot = bot
        self.dice_regex = r"\d+d\d+"

    @commands.command(name="roll", help="Simule un lancer de dés au format xDx")
    async def roll(self, ctx, *, calculation=""):
        """Rolls a dice in xDx format."""
        calculation = calculation.lower().strip()

        dices_expression = re.findall(
            pattern=self.dice_regex,
            string=calculation,
            flags=re.IGNORECASE
        )

        try:
            dice_results = []
            for dice in dices_expression:
                dice_results.append(self.process_dice(dice))
        except ValueError as e:
            response = "Ohh la flemme de lancer tous ces dés !"
        else:
            math_expression = calculation
            for dice_result in dice_results:
                math_expression = re.sub(
                    pattern=self.dice_regex,
                    repl=dice_result,
                    string=math_expression,
                    count=1,
                    flags=re.IGNORECASE
                )
            try:
                self.bot.log.warning(f"User {ctx.author.name} ({ctx.author.id}) asks to evaluate this expression: '{math_expression}' in this channel: {ctx.guild}, #{ctx.channel.name} ({ctx.channel.id})")
                total = self.eval_expr(math_expression)
            except (TypeError, SyntaxError) as e:
                response = "Ceci n'est pas une expression valide !"
            else:
                response = f"{ctx.author.mention}: **{total}** *({math_expression})*"

        await ctx.send(response)

    def process_dice(self, dice):
        number_of_dice, number_of_sides = map(int, dice.split('d'))
        if number_of_dice <= 200 and number_of_sides <= 200:
            dice_results = []
            for _ in range(number_of_dice):
                dice_results.append(secrets.randbelow(number_of_sides) + 1)

            return "(" + " + ".join(str(d) for d in dice_results) + ")"
        else:
            raise ValueError

    def eval_expr(self, expr):

        def eval_(node):
            # supported operators
            operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                         ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
                         ast.USub: op.neg}
            if isinstance(node, ast.Num):  # <number>
                return node.n
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return operators[type(node.op)](eval_(node.left), eval_(node.right))
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                return operators[type(node.op)](eval_(node.operand))
            else:
                raise TypeError(node)

        return eval_(ast.parse(expr, mode='eval').body)

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
                        "Désastre :rotating_light:"
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
                    response = "Merci de choisir un dé parmi : fortune (ou f), infortune (ou i), aptitude (ou a), maitrise (ou m), defi, force"
                    await ctx.send(response)
                    return

                dices = [secrets.choice(sides) for _ in range(number_of_dice)]
                response = f"{ctx.author.mention} : " + " + ".join(str(d) for d in dices)

            await ctx.send(response)
        except Exception as e:
            self.bot.log.error("Caught exception: ", exc_info=e)
            await ctx.send("Format has to be in xD<name>!")
