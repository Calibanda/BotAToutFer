# bot_init.py

import discord
from discord.ext import commands

import const
import set_logger

from package.on_message_jokes import on_message_jokes
from package.background_tasks import Tasks
from package.commands.cmd_discussion import Discussion
from package.commands.cmd_drinks import Drinks
from package.commands.cmd_green import Green
from package.commands.cmd_help import Help
from package.commands.cmd_ping import Ping
from package.commands.cmd_quotes import Quotes
from package.commands.cmd_roll_dice import Roll_dice
from package.commands.cmd_says import Says
from package.commands.cmd_utilitaries import Utilitaire

def bot_init():

    logger = set_logger.init()

    bot = commands.Bot(command_prefix="!", description=const.BOT_DESCRIPTION)
    bot.remove_command('help')


    @bot.event
    async def on_ready():
        """When the bot is connected to the guild, print guild informations"""
        print(f"Logged in as:\nUsername: {bot.user.name}\nUser ID: {bot.user.id}")
        logger.warning(f"Logged in as:\nUsername: {bot.user.name}\nUser ID: {bot.user.id}")
        print(f"{bot.user} is connected to the following guild(s):")
        for guild in bot.guilds:
            print(f"{guild.name} (id: {guild.id})")
            logger.warning(f"{bot.user} is connected to the following guild: {guild.name} (id: {guild.id})")
        
        # general_channels = discord.utils.get(bot.get_all_channels(), name="general")
        # print(general_channels)
        # print(channel.name for channel in bot.get_all_channels())
        # channel = discord.utils.get(client.get_all_channels(), guild__name='Cool', name='general')

        cat_channels = [bot.get_channel(763426416167485481)]  

        bot.add_cog(Tasks(bot, cat_channels, logger))
        bot.add_cog(Discussion(bot))
        bot.add_cog(Drinks(bot))
        bot.add_cog(Green(bot))
        bot.add_cog(Help(bot))
        bot.add_cog(Ping(bot))
        bot.add_cog(Quotes(bot))
        bot.add_cog(Roll_dice(bot))
        bot.add_cog(Says(bot))
        bot.add_cog(Utilitaire(bot, logger))

        # bot_channel = discord.utils.get(guild.channels, name=const.BOT_CHANNEL)


    @bot.event
    async def on_command_error(ctx, error):
        """When a command error occures displays the reason in the gild chat"""
        logger.error(f"On command error: {repr(error)}")
        if str(ctx.channel.id) == const.BOT_CHANNEL_ID:
            if isinstance(error, commands.errors.CheckFailure):
                await ctx.send("Nope, t'as pas le droit :P")
            else:
                await ctx.send("https://tenor.com/uqe8.gif") # Send a "C'est pas faux" gif


    @bot.event
    async def on_error(event, *args, **kwargs):
        logger.error(event, exc_info=args[0])
        raise


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if str(message.channel) == const.BOT_CHANNEL and message.content.startswith("!"):
            await bot.process_commands(message)
            return

        await on_message_jokes(bot, message)
    

    return bot
