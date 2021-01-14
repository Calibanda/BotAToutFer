# bot_init.py
import discord
from discord.ext import commands

import const
import logger_init

from package.on_message_jokes import on_message_jokes


def bot_init():
    """Create the Discord bot object with all configuration

    Returns:
        discord.ext.commands.Bot: The Discord bot client ready to go
    """
    bot = commands.Bot(command_prefix="!",
                       case_insensitive=True,
                       description=const.BOT_DESCRIPTION,
                       help_command=None,
                       activity=discord.Game(name=const.BOT_ACTIVITY),
                       owner_id=const.OWNER_ID
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

        bot.autorized_channels = [ bot.get_channel(channel_id) for channel_id in const.AUTORIZED_CHANNELS ]
        
        bot.load_extension("package.background_tasks")

        bot.load_extension("package.audio.music")
        bot.load_extension("package.commands.cmd_anniv")
        bot.load_extension("package.commands.cmd_discussion")
        bot.load_extension("package.commands.cmd_drinks")
        # bot.load_extension("package.commands.cmd_green")
        bot.load_extension("package.commands.cmd_help")
        bot.load_extension("package.commands.cmd_pendu")
        bot.load_extension("package.commands.cmd_ping")
        bot.load_extension("package.commands.cmd_quotes")
        bot.load_extension("package.commands.cmd_roll_dice")
        bot.load_extension("package.commands.cmd_santa")
        bot.load_extension("package.commands.cmd_says")
        bot.load_extension("package.commands.cmd_utilitaries")


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


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.content.startswith("!"):
            await bot.process_commands(message)
            return

        await on_message_jokes(bot, message)


    @bot.command()
    @commands.is_owner()
    async def load(ctx, name=None):
        if name:
            name = f"package.commands.cmd_{name}"
            try:
                bot.load_extension(name)
            except commands.errors.ExtensionNotFound as e:
                response = f"**L'extension *{name}* n'existe pas !**"
                await ctx.send(response)
            except commands.errors.ExtensionAlreadyLoaded as e:
                pass
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
            name = f"package.commands.cmd_{name}"
            try:
                bot.unload_extension(name)
            except commands.errors.ExtensionNotLoaded as e:
                response = f"**L'extension *{name}* n'était pas chargée !**"
                await ctx.send(response)
            else:
                response = f"L'extension *{name}* a bien été déchargée"
                await ctx.send(response)


    @bot.command()
    @commands.is_owner()
    async def reload(ctx, name=None):
        if name:
            original_name = name
            name = f"package.commands.cmd_{name}"
            try:
                bot.reload_extension(name)
            except commands.errors.ExtensionNotLoaded as e:
                await load(ctx, original_name)
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
        19/0


    return bot
