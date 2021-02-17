# bot_init.py
import os
import datetime
import json

from dotenv import load_dotenv
import discord
from discord.ext import commands


def bot_init():
    """Create the Discord bot object with all configuration

    Returns:
        discord.ext.commands.Bot: The Discord bot client ready to go
    """

    load_dotenv() # Loads sensitive constants form env

    # Create bot
    bot = commands.Bot(command_prefix="!",
                       case_insensitive=True,
                       description="BotAToutFer, le bot qui fait tout, même le café !",
                       help_command=None,
                       activity=discord.Game(name="!help"),
                       owner_id=int(os.getenv("OWNER_ID"))
    )

    # Add constants as variables in bot object
    bot.log = logger_init() # Add logger object to bot
    bot.SCRIPT_DIR = os.path.split(os.path.abspath(__file__))[0] # Add the absolute path to repo directory
    bot.TOKEN = os.getenv("DISCORD_TOKEN") # Add Discord bot token to bot

    bot.COFFEE_URL = os.getenv("COFFEE_URL")
    bot.COFFEE_PASSWORD = os.getenv("COFFEE_PASSWORD")

    bot.WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
    bot.NEWS_TOKEN = os.getenv("NEWS_TOKEN")
    bot.CAT_TOKEN = os.getenv("CAT_TOKEN")
    bot.DICOLINK_TOKEN = os.getenv("DICOLINK_TOKEN")


    @bot.event
    async def on_ready():
        """When the bot is connected to the guild, print guild informations"""
        print(f"Logged in as {bot.user} (user ID: {bot.user.id})")
        bot.log.warning(f"Logged in as {bot.user} (user ID: {bot.user.id})")
        print(f"{bot.user} is connected to the following guild(s):")
        for guild in bot.guilds:
            print(f"{guild.name} (id: {guild.id})")
            bot.log.warning(f"{bot.user} is connected to the following guild: {guild.name} (id: {guild.id})")

        bot.load_extension("extensions.anniv")
        bot.load_extension("extensions.dice")
        bot.load_extension("extensions.discussion")
        bot.load_extension("extensions.drinks")
        # bot.load_extension("extensions.green")
        bot.load_extension("extensions.help")
        bot.load_extension("extensions.message_jokes")
        # bot.load_extension("extensions.music")
        bot.load_extension("extensions.vbe_music")
        bot.load_extension("extensions.pendu")
        bot.load_extension("extensions.pictures")
        bot.load_extension("extensions.ping")
        bot.load_extension("extensions.quotes")
        # bot.load_extension("extensions.santa")
        bot.load_extension("extensions.says")
        bot.load_extension("extensions.utilitaries")


    @bot.event
    async def on_command_error(ctx, error):
        """When a command error occures displays the reason in the gild chat"""
        if hasattr(error, "original"):
            bot.log.error(f"Catched exeption:", exc_info=error.original)
        else:
            bot.log.error(f"Catched exeption:", exc_info=error)
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


    @bot.command()
    @commands.is_owner()
    async def load(ctx, name=None):
        if name:
            try:
                bot.load_extension(f"extensions.{name}")
            except commands.errors.ExtensionNotFound as e:
                response = f"**L'extension *{name}* n'existe pas !**"
                await ctx.send(response)
            except commands.errors.ExtensionAlreadyLoaded as e:
                await _reload(ctx, name)
            except commands.errors.ExtensionError as e:
                bot.log.error(f"Erreur avec l'extension {e.name}", exc_info=e)
                response = f"**Erreur avec l'extension {e.name}**"
                await ctx.send(response)
            else:
                response = f"L'extension *{name}* a bien été chargée"
                await ctx.send(response)


    @bot.command()
    @commands.is_owner()
    async def unload(ctx, name=None):
        if name:
            try:
                bot.unload_extension(f"extensions.{name}")
            except commands.errors.ExtensionNotLoaded as e:
                response = f"**L'extension *{name}* n'était pas chargée !**"
                await ctx.send(response)
            else:
                response = f"L'extension *{name}* a bien été déchargée"
                await ctx.send(response)


    @bot.command(name="reload")
    @commands.is_owner()
    async def _reload(ctx, name=None):
        if name:
            try:
                bot.reload_extension(f"extensions.{name}")
            except commands.errors.ExtensionNotLoaded as e:
                await load(ctx, name)
            except commands.errors.ExtensionNotFound as e:
                response = f"**L'extension *{name}* n'existe pas !**"
                await ctx.send(response)
            except commands.errors.ExtensionError as e:
                bot.log.error(f"Erreur avec l'extension {e.name}", exc_info=e)
                response = f"**Erreur avec l'extension {e.name}**"
                await ctx.send(response)
            else:
                response = f"L'extension *{name}* a bien été rechargée"
                await ctx.send(response)


    @bot.command()
    @commands.is_owner()
    async def zero(ctx):
        1/0


    return bot


def logger_init():
    """Create the logger object

    Returns:
        logging.Logger: The logger object ready to go
    """
    import logging

    script_dir, script_filename = os.path.split(os.path.abspath(__file__)) # Retreve the directory path of the script

    log_dir = os.path.join(script_dir, "logs") # The directory containing logs
    log_file_path = os.path.join(log_dir, datetime.datetime.now().strftime("%Y-%m-%d") + ".log") # Absolute path of the new log file

    if not os.path.exists(log_dir): # If the logs directory does not exist, we create it
        os.makedirs(log_dir)

    # Setting up the logging system
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(filename=log_file_path, encoding="utf-8", mode="a")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)

    return logger
