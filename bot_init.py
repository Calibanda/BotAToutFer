# bot_init.py
import traceback

import discord
from discord.ext import commands

import const
import logger_init

from package.on_message_jokes import on_message_jokes
from package.background_tasks import Tasks
from package.audio.music import Music
from package.commands.cmd_anniv import Anniversaire
from package.commands.cmd_discussion import Discussion
from package.commands.cmd_drinks import Drinks
from package.commands.cmd_green import Green
from package.commands.cmd_help import Help
from package.commands.cmd_pendu import Pendu
from package.commands.cmd_ping import Ping
from package.commands.cmd_quotes import Quotes
from package.commands.cmd_roll_dice import Roll_dice
from package.commands.cmd_santa import Santa
from package.commands.cmd_says import Says
from package.commands.cmd_utilitaries import Utilitaire


def bot_init():
    """Create the Discord bot object with all configuration

    Returns:
        discord.ext.commands.Bot: The Discord bot client ready to go
    """
    bot = commands.Bot(command_prefix="!",
                       case_insensitive=True,
                       description=const.BOT_DESCRIPTION,
                       help_command=None,
                       activity=discord.Game(name=const.BOT_ACTIVITY)
    )

    bot.log = logger_init.logger_init()


    @bot.event
    async def on_ready():
        """When the bot is connected to the guild, print guild informations"""
        print(f"Logged in as {bot.user} (user ID: {bot.user.id})")
        bot.log.warning(f"Logged in as {bot.user} (user ID: {bot.user.id})")
        print(f"{bot.user} is connected to the following guild(s):")
        for guild in bot.guilds:
            print(f"{guild.name} (id: {guild.id})")
            bot.log.warning(f"{bot.user} is connected to the following guild: {guild.name} (id: {guild.id})")

        bot.autorized_channel = [ bot.get_channel(channel_id) for channel_id in const.AUTORIZED_CHANNELS ]

        bot.add_cog(Tasks(bot))
        bot.add_cog(Music(bot))
        bot.add_cog(Anniversaire(bot))
        bot.add_cog(Discussion(bot))
        bot.add_cog(Drinks(bot))
        bot.add_cog(Green(bot))
        bot.add_cog(Help(bot))
        bot.add_cog(Pendu(bot))
        bot.add_cog(Ping(bot))
        bot.add_cog(Quotes(bot))
        bot.add_cog(Roll_dice(bot))
        bot.add_cog(Santa(bot))
        bot.add_cog(Says(bot))
        bot.add_cog(Utilitaire(bot))


    @bot.event
    async def on_command_error(ctx, error):
        """When a command error occures displays the reason in the gild chat"""
        bot.log.exception(f"Catched exeption:")
        if ctx.channel in bot.autorized_channel:
            if isinstance(error, commands.errors.CheckFailure):
                await ctx.send("Nope, t'as pas le droit :P")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("https://tenor.com/bmqvT.gif") # Send a "Did you forget something?" gif
            elif isinstance(error, discord.HTTPException):
                await ctx.send("https://tenor.com/bmQvt.gif") # Send a "Far too long" gif
            elif isinstance(error, commands.CommandNotFound):
                await ctx.send("https://tenor.com/uqe8.gif") # Send a "C'est pas faux" gif
            else:
                await ctx.send("https://tenor.com/bj9EB.gif") # Send an error gif


    @bot.event
    async def on_error(event, *args, **kwargs):
        bot.log.exception(f"Catched exeption:")


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.channel in bot.autorized_channel and message.content.startswith("!"):
            await bot.process_commands(message)
            return

        await on_message_jokes(bot, message)


    return bot
