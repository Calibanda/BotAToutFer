#!/usr/bin/env python3
"""The BotÀToutFer Discord bot

Copyright (C) 2022, Clément SEIJIDO
Released under GNU General Public License v3.0 (GNU GPLv3)
e-mail clement@seijido.fr

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import ApplicationContext


def initialize_logger(level: int, name: str) -> None:
    """Initialize logging system.

    Args:
        level (int): The level of logging (e.g. logging.DEBUG).
        name (str): The name of the log file.
    """
    # Retrieve the directory path of the script
    script_dir = pathlib.Path(__file__).resolve().parent

    # The directory containing logs
    log_dir = script_dir / 'logs'
    # Create log_dir if needed
    log_dir.mkdir(parents=True, exist_ok=True)

    # Absolute path of the new log file
    log_file_path = log_dir / f'{name}.log'

    # Setting up the logging system
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when='midnight',
        backupCount=5,
        encoding='utf-8'
    )
    handler.suffix = '%Y-%m-%d.log'
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    )

    logger.addHandler(handler)


def main() -> None:
    load_dotenv()  # load sensitive constants form .env file

    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or('!'),
        case_insensitive=True,
        description="BotAToutFer, le bot qui fait tout, même le café !",
        help_command=None,
        activity=discord.Activity(
            name='Now with slash commands!',
            type=discord.ActivityType.playing
        ),
        # debug_guilds=set(map(int, os.getenv('DEBUG_GUILDS').split(';'))),
        owner_ids=set(map(int, os.getenv('OWNER_IDS').split(';')))
    )

    log = logging.getLogger(__name__)
    log.info('Starting bot')

    script_dir = pathlib.Path(__file__).resolve().parent
    cog_directory = script_dir / 'cogs'
    cogs_to_load = [
        f'cogs.{cog.stem}' for cog in cog_directory.iterdir()
        if cog.is_file() and not cog.name.startswith('.')
    ]

    cogs_to_load.sort()

    for cog in cogs_to_load:
        try:
            bot.load_extension(cog)
        except discord.ExtensionError as e:
            log.error(f'Error with extension {e.name}', exc_info=e)
            print(f'Error with extension {e.name}')

    # ensure the 'package' directory exists
    (script_dir / 'package').mkdir(parents=True, exist_ok=True)

    @bot.event
    async def on_ready():
        """When bot is ready, display and log useful information.
        """
        print(f'Logged in as {bot.user} (user ID: {bot.user.id})')
        log.info(f'Logged in as {bot.user} (user ID: {bot.user.id})')
        print(f'{bot.user} is connected to the following guild(s):')
        for guild in bot.guilds:
            print(f'{guild.name} (id: {guild.id})')
            log.info(
                f'{bot.user} is connected to the following guild: '
                f'{guild.name} (id: {guild.id})'
            )

    def process_error(error: Exception) -> str:
        """Log a given error and return an associated joke.

        Args:
            error (Exception): the exception to handle.

        Returns:
            str: the joke to send in Discord channel.
        """
        if hasattr(error, 'original'):
            log.error('Caught exception:', exc_info=error.original)
        else:
            log.error('Caught exception:', exc_info=error)
        if isinstance(error, commands.errors.CheckFailure):
            return "Nope, t'as pas le droit :P"
        elif isinstance(error, commands.MissingRequiredArgument):
            return 'https://tenor.com/bmqvT.gif'  # 'Did you forget something?'
        elif isinstance(error, commands.errors.UserNotFound):
            return 'https://tenor.com/bg6ud.gif'  # 'WHO DAT?'
        elif 'Author not connected to a voice channel.' in str(error):
            return 'You are not connected to a voice channel.'
        elif isinstance(error, discord.HTTPException):
            return 'https://tenor.com/bmQvt.gif'  # 'Far too long'
        elif isinstance(error, commands.CommandNotFound):
            return 'https://tenor.com/uqe8.gif'  # "C'est pas faux"
        else:
            return 'https://tenor.com/bj9EB.gif'  # error

    @bot.event
    async def on_command_error(ctx: commands.Context, error: Exception):
        """When a command error occurs, displays the reason in gild chat.
        """
        response = process_error(error)
        await ctx.message.reply(response)

    @bot.event
    async def on_application_command_error(
            ctx: ApplicationContext,
            error: Exception
    ):
        """When a command error occurs, displays the reason in gild chat.
        """
        response = process_error(error)
        await ctx.respond(response)

    @bot.event
    async def on_error(event: str, *args, **kwargs):
        """On error, log the occurred exception.
        """
        log.exception(
            f'Caught on_error exception, {event=}, {args=}, {kwargs=}:'
        )

    @bot.command()
    @commands.is_owner()
    async def load(ctx: commands.Context, extension_name: str):
        """Load a given extension. Reserved to bot owner(s).
        """
        if extension_name:
            try:
                bot.load_extension(f'cogs.{extension_name}')
            except discord.ExtensionNotFound:
                response = f'**Extension *{extension_name}* does not exist!**'
                await ctx.message.reply(response)
            except discord.ExtensionAlreadyLoaded:
                await _reload(ctx, extension_name)
            except discord.ExtensionError as e:
                log.error(f'Error with extension {e.name}', exc_info=e)
                response = f'**Error with extension {e.name}**'
                await ctx.message.reply(response)
            else:
                response = f'Extension *{extension_name}* has been loaded'
                await ctx.message.reply(response)

    @bot.command()
    @commands.is_owner()
    async def unload(ctx: commands.Context, extension_name: str):
        """Unload a given extension. Reserved to bot owner(s).
        """
        if extension_name:
            try:
                bot.unload_extension(f'cogs.{extension_name}')
            except discord.ExtensionNotLoaded:
                response = f'**The extension *{extension_name}* was ' \
                           f'not loaded**'
                await ctx.message.reply(response)
            else:
                response = f'Extension *{extension_name}* unloaded'
                await ctx.message.reply(response)

    @bot.command(name='reload')
    @commands.is_owner()
    async def _reload(ctx: commands.Context, extension_name: str):
        """Reload a given extension. Reserved to bot owner(s).
        """
        if extension_name:
            try:
                bot.reload_extension(f'cogs.{extension_name}')
            except discord.ExtensionNotLoaded:
                await load(ctx, extension_name)
            except discord.ExtensionNotFound:
                response = f'**Extension *{extension_name}* does not exist!**'
                await ctx.message.reply(response)
            except discord.ExtensionError as e:
                log.error(f'Error with extension {e.name}', exc_info=e)
                response = f'**Error with extension {e.name}**'
                await ctx.message.reply(response)
            else:
                response = f'Extension *{extension_name}* reloaded'
                await ctx.message.reply(response)

    @bot.command(name='reload-all')
    @commands.is_owner()
    async def reload_all(ctx: commands.Context):
        """Reload all loaded extensions. Reserved to bot owner(s).
        """
        extension_to_reload = [ext for ext in bot.extensions.keys()]
        for extension in extension_to_reload:
            try:
                bot.reload_extension(extension)
            except discord.ExtensionNotFound:
                response = f'**Extension *{extension}* does not exist!**'
                await ctx.message.reply(response)
            except discord.ExtensionError as e:
                log.error(f'Error with extension {e.name}', exc_info=e)
                response = f'**Error with extension {e.name}**'
                await ctx.message.reply(response)

        response = 'All extensions reloaded'
        await ctx.message.reply(response)

    @bot.command()
    @commands.is_owner()
    async def zero(ctx: commands.Context):
        """Generate a ZeroDivisionError. Reserved to bot owner(s).
        """
        1/0

    bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    initialize_logger(logging.INFO, 'discord')
    main()
