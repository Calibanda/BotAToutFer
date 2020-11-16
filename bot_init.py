# bot_init.py

import discord
from discord.ext import commands

import const
import set_logger

from package.on_message_jokes import on_message_jokes
from package.background_tasks import Tasks
#from package.audio.music import Music
from package.commands.cmd_discussion import Discussion
from package.commands.cmd_drinks import Drinks
from package.commands.cmd_green import Green
from package.commands.cmd_help import Help
from package.commands.cmd_pendu import Pendu
from package.commands.cmd_ping import Ping
from package.commands.cmd_quotes import Quotes
from package.commands.cmd_roll_dice import Roll_dice
from package.commands.cmd_says import Says
from package.commands.cmd_utilitaries import Utilitaire


def bot_init():

    bot = commands.Bot(command_prefix="!", description=const.BOT_DESCRIPTION, case_insensitive=True)
    bot.remove_command('help')

    bot.log = set_logger.init()


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
        #bot.add_cog(Music(bot))
        bot.add_cog(Discussion(bot))
        bot.add_cog(Drinks(bot))
        bot.add_cog(Green(bot))
        bot.add_cog(Help(bot))
        bot.add_cog(Pendu(bot))
        bot.add_cog(Ping(bot))
        bot.add_cog(Quotes(bot))
        bot.add_cog(Roll_dice(bot))
        bot.add_cog(Says(bot))
        bot.add_cog(Utilitaire(bot))


    @bot.event
    async def on_command_error(ctx, error):
        """When a command error occures displays the reason in the gild chat"""
        error_name = error.__class__.__name__
        bot.log.error(f"{error_name}: {error}")
        if ctx.channel in bot.autorized_channel:
            if isinstance(error, commands.errors.CheckFailure):
                await ctx.send("Nope, t'as pas le droit :P")
            elif isinstance(error, discord.HTTPException):
                await ctx.send("https://tenor.com/bmQvt.gif") # Send a "Far too long" gif
            else:
                await ctx.send("https://tenor.com/uqe8.gif") # Send a "C'est pas faux" gif


    @bot.event
    async def on_error(event, *args, **kwargs):
        bot.log.error(event, exc_info=args[0])
        raise


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.channel in bot.autorized_channel and message.content.startswith("!"):
            await bot.process_commands(message)
            return

        await on_message_jokes(bot, message)


    return bot
