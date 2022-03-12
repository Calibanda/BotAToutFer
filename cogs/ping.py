"""Ping command for the BotÀToutFer Discord bot

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

import logging
import pathlib
import __main__

import discord
from discord.ext import commands
from discord import ApplicationContext


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Ping(bot))


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log = logging.getLogger(__name__)
        self.script_dir = pathlib.Path(__main__.__file__).resolve().parent

        self.log.info(f'Load {__class__.__name__}')

    @commands.slash_command(name='ping')
    async def ping(self, ctx: ApplicationContext):
        """Respond pong.
        """
        response = f'pong (latency: {round(self.bot.latency * 1000)}ms)'
        await ctx.respond(response)
