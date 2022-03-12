"""Dice commands for the BotÀToutFer Discord bot

Copyright (C) 2022, Clément SEIJIDO
Released under GNU General Public License v3.0 (GNU GPLv3)
e-mail clement@seijido.fr

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import pathlib
import __main__
import secrets
import re
import ast
import operator as op

import discord
from discord.ext import commands
from discord import ApplicationContext


def setup(bot: commands.Bot) -> None:
    bot.add_cog(DiceRolls(bot))


class DiceRolls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log = logging.getLogger(__name__)
        self.script_dir = pathlib.Path(__main__.__file__).resolve().parent

        self.dice_regex = r'\d+d\d+'

        self.log.info(f'Load {__class__.__name__}')

    @commands.slash_command(name='roll')
    async def roll(self, ctx: ApplicationContext, *, dice_expression: str):
        """Rolls a dice in xDx format.
        """
        dice_expression = dice_expression.lower().strip()

        dices_expression = re.findall(
            pattern=self.dice_regex,
            string=dice_expression,
            flags=re.IGNORECASE
        )

        try:
            dice_results = []
            for dice in dices_expression:
                dice_results.append(self.process_dice(dice))
        except ValueError:
            response = 'Ohh la flemme de lancer tous ces dés !'
        else:
            math_expr = dice_expression
            for dice_result in dice_results:
                # replace all xDx by the previous calculated values
                math_expr = re.sub(
                    pattern=self.dice_regex,
                    repl=dice_result,
                    string=math_expr,
                    count=1,
                    flags=re.IGNORECASE
                )
            try:
                self.log.warning(
                    f'User {ctx.author.name} ({ctx.author.id}) asks to '
                    f'evaluate this expression: "{math_expr}" in this '
                    f'channel: {ctx.guild}, #{ctx.channel.name} '
                    f'({ctx.channel.id})'
                )
                total = self.eval_expr(math_expr)
            except (TypeError, SyntaxError):
                response = 'Invalid expression. Use xDx format'
            else:
                response = f'{ctx.author.mention}: **{total}** *(' \
                           f'{discord.utils.escape_markdown(math_expr)}' \
                           f' = **{total}**)*'

        await ctx.respond(response)

    def process_dice(self, dice: str) -> str:
        """Resolve a xDx dice expression
        """
        number_of_dice, number_of_sides = map(int, dice.split('d'))
        if number_of_dice <= 200 and number_of_sides <= 200:
            dice_results = []
            for _ in range(number_of_dice):
                dice_results.append(secrets.randbelow(number_of_sides) + 1)

            return '(' + ' + '.join(str(d) for d in dice_results) + ')'
        else:
            raise ValueError

    def eval_expr(self, expr):
        def eval_(node):
            operators = {  # supported operators
                ast.Add: op.add,
                ast.Sub: op.sub,
                ast.Mult: op.mul,
                ast.Div: op.truediv,
                ast.Pow: op.pow,
                ast.BitXor: op.xor,
                ast.USub: op.neg
            }
            if isinstance(node, ast.Num):  # <number>
                return node.n
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return operators[type(node.op)](
                    eval_(node.left),
                    eval_(node.right)
                )
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand>
                return operators[type(node.op)](eval_(node.operand))
            else:
                raise TypeError(node)

        return eval_(ast.parse(expr, mode='eval').body)
