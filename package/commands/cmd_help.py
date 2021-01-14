# help command for BotÀToutFer
import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Help(bot))


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.command(name="help", help="Affiche ce message", pass_context=True)
    async def help(self, ctx, command=""):
        response = f"```\n{self.bot.description}\n\n"

        list_cogs = sorted([ cog for cog in self.bot.cogs if not hasattr(self.bot.get_cog(cog), "hidden_cog") or not self.bot.get_cog(cog).hidden_cog ])
        number_spaces = len(sorted([c.name for c in self.bot.commands], key=lambda command: len(command))[-1]) + 1

        for cog in list_cogs:
            response += f"{cog} :\n"

            for command in sorted(self.bot.get_cog(cog).get_commands(), key=lambda command: command.name):
                response += "  " + command.name.ljust(number_spaces, " ") + f"{command.help}\n"

            response += "\n"

        response += "```"

        await ctx.send(response)
