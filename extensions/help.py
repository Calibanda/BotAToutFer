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
        response = f"```\n{self.bot.description}\n\n" # We create a new response string

        list_cogs = sorted([ cog for cog in self.bot.cogs if not hasattr(self.bot.get_cog(cog), "hidden_cog") or not self.bot.get_cog(cog).hidden_cog ])
        number_spaces = len(sorted([c.name for c in self.bot.commands], key=lambda command: len(command))[-1]) + 1

        for cog in list_cogs:
            cog_help = f"{cog} :\n" # We create the new cog hepl string
            for command in sorted(self.bot.get_cog(cog).get_commands(), key=lambda command: command.name):
                cog_help += "  " + command.name.ljust(number_spaces, " ") + f"{command.help}\n"

            if len(response + cog_help) + 3 < 2000: # If next help can be added without exeed the Discord limit
                response += cog_help # We add the cog help to the response
            else: # If cog help CANNOT be added without exeed the Discord limit
                response += "```"
                await ctx.send(response) # We send the response
                response = "```\n" # We create a new response
                response += cog_help # We add the cog help to the new response
        if len(response) > 3:# We exhaust all the cogs, we send the cog help if any
            response += "```"
            await ctx.send(response) 
