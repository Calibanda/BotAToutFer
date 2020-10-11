# help command for BotAToutFer
import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot, bot_channel_id):
        self.bot = bot
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="help", help="Affiche ce message", pass_context=True)
    async def help(self, ctx, command=""):
        if str(ctx.channel.id) == self.bot_channel_id:
            response = f"```\n{self.bot.description}\n\n"

            list_cogs = sorted([ cog for cog in self.bot.cogs ])
            number_spaces = len(sorted([c.name for c in self.bot.commands], key=lambda command: len(command))[-1]) + 1

            for cog in list_cogs:
                response += f"{cog} :\n"

                for command in sorted(self.bot.get_cog(cog).get_commands(), key=lambda command: command.name):
                    response += "  " + command.name.ljust(number_spaces, " ") + f"{command.help}\n"

                response += "\n"

            response += "Taper '!help commande' pour avoir plus d'infos sur cette commande.\n```"

            await ctx.send(response)
