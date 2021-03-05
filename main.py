# main.py
import os
import json

from dotenv import load_dotenv
import discord
from discord.ext import commands


def bot_init():
    """Create and return the Discord bot object with all configuration

    Returns:
        discord.ext.commands.Bot: The Discord bot client ready to go
    """

    load_dotenv()  # Loads sensitive constants form env

    # Create bot
    bot = commands.Bot(command_prefix="!",
                       case_insensitive=True,
                       description=("BotAToutFer, le bot qui fait tout, "
                       + "même le café !"),
                       help_command=None,
                       activity=discord.Game(name="!help"),
                       owner_id=int(os.getenv("OWNER_ID"))
                       )

    # Add constants as variables in bot object

    bot.log = logger_init()  # Add logger object to bot
    # Add the absolute path to repo directory
    bot.SCRIPT_DIR = os.path.split(os.path.abspath(__file__))[0]
    bot.TOKEN = os.getenv("DISCORD_TOKEN")  # Add Discord bot token to bot

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
            bot.log.warning(
                f"{bot.user} is connected to the following guild: "
                + f"{guild.name} (id: {guild.id})"
                )

        extensions_to_load = [
            "anniv",
            "boules",
            "dice",
            "discussion",
            # "drinks",
            # "green",
            "help",
            "message_jokes",
            # "music",
            "pendu",
            "pictures",
            "ping",
            "quotes",
            # "santa",
            "says",
            "utilitaries",
            "vbe_music",
        ]

        for extension in extensions_to_load:
            try:
                bot.load_extension(f"extensions.{extension}")
            except commands.errors.ExtensionError as e:
                bot.log.error(f"Erreur avec l'extension {e.name}", exc_info=e)
                print(f"Erreur avec l'extension {e.name}")

    @bot.event
    async def on_command_error(ctx, error):
        """When a command error occures displays the reason in gild chat"""
        if hasattr(error, "original"):
            bot.log.error(f"Catched exeption:", exc_info=error.original)
        else:
            bot.log.error(f"Catched exeption:", exc_info=error)
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("Nope, t'as pas le droit :P")
        elif isinstance(error, commands.MissingRequiredArgument):
            # Send a "Did you forget something?" gif
            await ctx.send("https://tenor.com/bmqvT.gif")
        elif isinstance(error, discord.HTTPException):
            # Send a "Far too long" gif
            await ctx.send("https://tenor.com/bmQvt.gif")
        elif isinstance(error, commands.CommandNotFound):
            # Send a "C'est pas faux" gif
            await ctx.send("https://tenor.com/uqe8.gif")
        else:
            # Send an error gif
            await ctx.send("https://tenor.com/bj9EB.gif")

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

    @bot.command(name="reload-all")
    @commands.is_owner()
    async def reload_all(ctx):
        for extension in bot.extensions:
            try:
                bot.reload_extension(f"extensions.{extension}")
            except commands.errors.ExtensionNotFound as e:
                response = f"**L'extension *{e.name}* n'existe pas !**"
                await ctx.send(response)
            except commands.errors.ExtensionError as e:
                bot.log.error(f"Erreur avec l'extension {e.name}", exc_info=e)
                response = f"**Erreur avec l'extension {e.name}**"
                await ctx.send(response)

        response = "Extensions rechargées"
        await ctx.send(response)

    @bot.command()
    @commands.is_owner()
    async def zero(ctx):
        1/0

    return bot


def logger_init():
    """Create and return the logger object

    Returns:
        logging.Logger: The logger object ready to go
    """
    import logging
    from logging.handlers import TimedRotatingFileHandler

    # Retreve the directory path of the script
    script_dir, script_filename = os.path.split(os.path.abspath(__file__))

    # The directory containing logs
    log_dir = os.path.join(script_dir, "logs")
    # Absolute path of the new log file
    log_file_path = os.path.join(log_dir, "botatoutfer.log")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Setting up the logging system
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when='midnight',
        interval=1,
        encoding="utf-8"
    )
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    bot = bot_init()
    bot.run(bot.TOKEN)
