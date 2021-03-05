# help command for BotÀToutFer
import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Help(bot))


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(
        name="help",
        help="Affiche ce message",
        pass_context=True
    )
    async def help(self, ctx, command=""):
        response = f"```\n{self.bot.description}\n\n"  # Create a new response

        list_cogs = []
        for cog in self.bot.cogs:
            if (not hasattr(self.bot.get_cog(cog), "hidden_cog")
                    or not self.bot.get_cog(cog).hidden_cog):
                # If the cog has no attribute "hidden_cog"
                # or if this attribute is false
                list_cogs.append(cog)

        list_cogs = sorted(list_cogs)

        command_names = [c.name for c in self.bot.commands]
        command_names = sorted(  # Sort list by length
            command_names,
            key=lambda command: len(command)
        )

        number_spaces = len(command_names[-1]) + 1

        for cog in list_cogs:
            cog_help = f"{cog} :\n"  # We create the new cog help string
            alphabetical_cogs = sorted(
                self.bot.get_cog(cog).get_commands(),
                key=lambda command: command.name
            )

            for command in alphabetical_cogs:
                cog_help += (
                    "  "
                    + command.name.ljust(number_spaces, " ")
                    + f"{command.help}\n"
                )
            cog_help += "\n"

            if len(response + cog_help) + 3 < 2000:
                # If next help can be added without exeed the Discord limit
                response += cog_help  # We add the cog help to the response
            else:
                # If cog help CANNOT be added without exeed the Discord limit
                response += "```"
                await ctx.send(response)  # We send the response
                response = "```\n"  # We create a new response
                response += cog_help  # We add cog help to the new response

        if len(response) > 3:
            # We exhaust all the cogs, we send the cog help if any
            response += "```"
            await ctx.send(response)
