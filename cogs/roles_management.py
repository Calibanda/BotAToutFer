"""Role management commands for the BotÀToutFer Discord bot

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
import datetime
import json
import asyncio

import discord
from discord.ext import commands, tasks
from discord import ApplicationContext
from discord.commands import permissions, Option


def setup(bot: commands.Bot) -> None:
    bot.add_cog(RolesManagement(bot))


class RoleManagerMessage:
    def __init__(
            self,
            message: discord.Message,
            role: discord.Role,
            gm: discord.Member | discord.User,
            creation_time: float = None
    ):
        self.message = message
        self.role = role
        self.gm = gm
        if creation_time is None:
            self.creation_time = datetime.datetime.now()
        else:
            self.creation_time = datetime.datetime.fromtimestamp(creation_time)

    def __iter__(self):
        yield from {
            'guild_id': self.message.guild.id,
            'channel_id': self.message.channel.id,
            'message_id': self.message.id,
            'role_id': self.role.id,
            'gm_id': self.gm.id,
            'creation_timestamp': self.creation_time.timestamp()
        }.items()

    def __str__(self) -> str:
        return json.dumps(dict(self))

    def __repr__(self) -> str:
        return self.__str__()


class RolesManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log = logging.getLogger(__name__)
        self.script_dir = pathlib.Path(__main__.__file__).resolve().parent

        # ensure the 'package' directory exists
        self.package_dir = self.script_dir / 'package'
        self.package_dir.mkdir(parents=True, exist_ok=True)

        self.role_manager_json = self.package_dir / 'role_managers.json'

        self.gm_role_id = 949935758981091328  # 812989543229685800

        self.role_manager_messages: list[RoleManagerMessage] = []

        self.log.info(f'Load {__class__.__name__}')

        # @self.bot.message_command(name='Show ID', default_permission=False)
        # @permissions.permission(role_id=self.gm_role_id, permission=True)
        # async def show_id(
        #         ctx: ApplicationContext,
        #         message: discord.Message,
        #         role: Option(discord.Role, "Select a role")
        # ):
        #     await ctx.respond(
        #         f"{ctx.author.name}, here's the message id: {message.id} "
        #         f"and the role id: {role.id}!",
        #     )

    @commands.Cog.listener('on_ready')
    async def fill_role_manager_messages(self):
        if not self.role_manager_json.is_file():
            return

        with open(self.role_manager_json, 'r') as f:
            raw_messages = json.load(f)

        for m in raw_messages:
            try:
                guild = self.bot.get_guild(m['guild_id'])
                channel = guild.get_channel(m['channel_id'])
                message = await channel.fetch_message(m['message_id'])
                gm = guild.get_member(m['gm_id'])
                creation_time = m['creation_timestamp']
                role = guild.get_role(m['role_id'])

                self.role_manager_messages.append(RoleManagerMessage(
                    message=message,
                    role=role,
                    gm=gm,
                    creation_time=creation_time
                ))

            except Exception as e:
                self.log.exception('Unable to recreate a role manager')

    def cog_unload(self):
        self.old_messages_cleaning_loop.cancel()

    @tasks.loop(hours=24)
    async def old_messages_cleaning_loop(self):
        self.log.info('Start old messages cleaning loop')

        now = datetime.datetime.now()

        self.role_manager_messages = [  # only keep messages younger than 15 d
            message for message in self.role_manager_messages
            if now - message.creation_time < datetime.timedelta(days=15)
        ]

        self.save_role_manager_messages()

    @old_messages_cleaning_loop.before_loop
    async def before_old_messages_cleaning_loop(self):
        await self.bot.wait_until_ready()

        self.log.info('Start before_old_messages_cleaning_loop')

        alarm = datetime.datetime.now().replace(
            hour=6,
            minute=0,
            second=0,
            microsecond=0
        )
        delta = (alarm - datetime.datetime.now()).total_seconds()
        if delta < 0:  # 6AM is passed today
            delta += datetime.timedelta(days=1).total_seconds()

        self.log.info(f'sleep {delta} seconds')
        await asyncio.sleep(delta)  # await next 6AM

    @old_messages_cleaning_loop.error
    async def error_old_messages_cleaning_loop(self, e: Exception):
        self.log.error('Error during old messages cleaning loop', exc_info=e)
        self.old_messages_cleaning_loop.restart()

    @commands.Cog.listener('on_raw_reaction_add')
    async def add_role(
            self,
            payload: discord.RawReactionActionEvent
    ):
        """Add a role to user if needed
        """
        for role_manager_message in self.role_manager_messages:
            if payload.message_id == role_manager_message.message.id:

                if payload.user_id == role_manager_message.gm.id:
                    # does not want to modify the gm roles
                    return

                guild = await self.bot.fetch_guild(payload.guild_id)
                member = await guild.fetch_member(payload.user_id)

                await member.add_roles(
                    role_manager_message.role,
                    reason='User added a reaction to a role manager message!'
                )

                await role_manager_message.gm.send(
                    f'{payload.member} joined your adventure '
                    f'{role_manager_message.role.name}'
                )

    @commands.Cog.listener('on_raw_reaction_remove')
    async def remove_role(
            self,
            payload: discord.RawReactionActionEvent
    ):
        """Add a role to user if needed
        """
        for role_manager_message in self.role_manager_messages:
            if payload.message_id == role_manager_message.message.id:

                if payload.user_id == role_manager_message.gm.id:
                    # does not want to modify the gm roles
                    return

                guild = await self.bot.fetch_guild(payload.guild_id)
                member = await guild.fetch_member(payload.user_id)

                await member.remove_roles(
                    role_manager_message.role,
                    reason='User removed a reaction to a role manager message!'
                )

                await role_manager_message.gm.send(
                    f'{member} left your adventure '
                    f'{role_manager_message.role.name}'
                )

    @commands.slash_command(name='add-role-message', default_permission=False)
    @permissions.permission(role_id=949935758981091328, permission=True)
    async def add_role_manager_message(
            self,
            ctx: ApplicationContext,
            message_id: discord.Message,
            role: Option(discord.Role)
    ):
        self.role_manager_messages.append(RoleManagerMessage(
            message=message_id,
            role=role,
            gm=ctx.author
        ))

        await ctx.respond(
            f'{ctx.author.mention}, saved this message: '
            f'"{message_id.content}" as manager of this role: {role.mention}!',
            ephemeral=True
        )

        self.save_role_manager_messages()

    def save_role_manager_messages(self):
        with open(self.role_manager_json, 'w') as f:
            # save role_manager_messages on disk
            json.dump(
                obj=[dict(m) for m in self.role_manager_messages],
                fp=f,
                indent=4
            )
