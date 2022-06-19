"""Music commands for the BotÀToutFer Discord bot

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
import math
import random
import datetime
import asyncio
import itertools
import collections
import subprocess

import yt_dlp
import discord
from discord.ext import commands, tasks
from discord import ApplicationContext

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Music(bot))


class NotConnectedToVoiceChannelError(discord.DiscordException):
    def __init__(self):
        super().__init__('Author not connected to a voice channel.')


class CustomYoutubeDLLogger:
    def __init__(self, logger: logging.Logger):
        self.log = logger

    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed
        # into debug. You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            self.log.debug(msg)
        else:
            self.info(msg)

    def info(self, msg):
        self.log.info(msg)

    def warning(self, msg):
        self.log.warning(msg)

    def error(self, msg):
        self.log.error(msg)


class Song:
    def __init__(
            self,
            ctx: ApplicationContext,
            source: str | pathlib.Path,
            duration: int = None,
            url: str = None,
            title: str = None,
            thumbnail: str = None
    ):
        self.requester = ctx.author
        self.request_channel = ctx.channel
        self.filename = pathlib.Path(source).resolve()
        self.url = url
        self.title = title if title is not None else self.filename.stem
        self.thumbnail = thumbnail

        try:
            self.duration = self.parse_duration(duration)
        except (TypeError, ValueError):
            self.duration = 'No duration'

    def parse_duration(self, duration):
        if duration is None:
            process = subprocess.Popen(
                (
                    'ffprobe',
                    '-v',
                    'error',
                    '-show_entries',
                    'format=duration',
                    '-of',
                    'default=noprint_wrappers=1:nokey=1',
                    '-i',
                    f'{self.filename}'
                ),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            stdout, stderr = process.communicate()
            duration = math.ceil(float(stdout.decode()))

        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f'{days} days')
        if hours > 0:
            duration.append(f'{hours} hours')
        if minutes > 0:
            duration.append(f'{minutes} minutes')
        if seconds > 0:
            duration.append(f'{seconds} seconds')

        return ', '.join(duration)

    def create_embed(self):
        embed = discord.Embed(
            title='Now playing',
            description=f'```\n{self.title}\n```',
            color=discord.Color.blurple()
        )
        embed.add_field(name='Duration', value=self.duration)
        embed.set_author(
            name=self.requester.name,
            icon_url=self.requester.avatar.url
        )
        embed.add_field(name='Requested by', value=self.requester.mention)
        if self.url is not None:
            embed.add_field(
                name='URL',
                value=f'[Click]({self.url})'
            )

        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)

        return embed


class SongQueue(asyncio.Queue):
    def __init__(self):
        self._queue = collections.deque()
        super().__init__()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(
                self._queue, item.start, item.stop, item.step
            ))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class Jukebox:
    def __init__(self, ctx: ApplicationContext):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.text_channel = ctx.channel
        self.voice_client: discord.VoiceClient = ctx.voice_client

        self.log = logging.getLogger(__name__)

        # signal between async functions
        self.ready_for_next_song = asyncio.Event()

        self.songs = SongQueue()
        self.current_song = None
        self.timeout = 3 * 60  # 3 minutes

        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        return self.voice_client \
               and self.current_song \
               and self.voice_client.is_playing()

    def start(self):
        """Ensure the audio_player task is running.
        """
        if self.audio_player.cancelled():
            self.audio_player = self.bot.loop.create_task(
                self.audio_player_task()
            )

    async def stop(self):
        """Empty the queue, cancel the task and disconnect voice client.
        """
        self.songs.clear()
        if not self.audio_player.cancelled():
            self.audio_player.cancel()

        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None

    def skip(self):
        """Skip current song.
        """
        if self.is_playing():
            self.voice_client.stop()

    async def audio_player_task(self):
        while True:
            self.ready_for_next_song.clear()  # clear signal

            try:
                # Try to get the next song within the timeout.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance reasons.
                self.current_song: Song = await asyncio.wait_for(
                    fut=self.songs.get(),
                    timeout=self.timeout
                )

            except asyncio.TimeoutError:
                self.bot.loop.create_task(self.stop())
                return

            try:
                self.voice_client.play(
                    source=discord.PCMVolumeTransformer(
                        discord.FFmpegPCMAudio(
                            self.current_song.filename.as_posix()
                        )
                    ),
                    after=self.after_play
                )

                await self.current_song.request_channel.send(
                    embed=self.current_song.create_embed()
                )
            except Exception:
                self.log.exception('Exception in Jukebox: ')

            await self.ready_for_next_song.wait()  # wait for signal

    def after_play(self, error: Exception = None):
        if error is not None:
            self.log.exception('Error during music: ')

        self.ready_for_next_song.set()  # send signal


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log = logging.getLogger(__name__)
        self.script_dir = pathlib.Path(__main__.__file__).resolve().parent

        # The directory containing musics
        self.music_dir = self.script_dir / 'music'
        # Create music_dir if needed
        self.music_dir.mkdir(parents=True, exist_ok=True)

        # The directory containing ytdl_downloads
        self.ytdl_dir = self.music_dir / 'ytdl'
        # Create ytdl_dir if needed
        self.ytdl_dir.mkdir(parents=True, exist_ok=True)

        self.ytdl_options = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.ytdl_dir}/%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nooverwrites': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'logger': CustomYoutubeDLLogger(self.log),
            'source_address': '0.0.0.0',  # Bind to ipv4
        }
        self.ffmpeg_options = {'options': '-vn'}

        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_options)

        self.jukeboxes = {}

        self.audio_files_cleaning_loop.start()

        self.log.info(f'Load {__class__.__name__}')

    def cog_unload(self):
        self.audio_files_cleaning_loop.cancel()
        for jukebox in self.jukeboxes.values():
            self.bot.loop.create_task(jukebox.stop())

    @tasks.loop(hours=24)
    async def audio_files_cleaning_loop(self):
        self.log.info('Start audio files cleaning loop')

        now = datetime.datetime.now()

        for file in self.ytdl_dir.iterdir():
            if not file.is_file():
                continue

            st_atime = datetime.datetime.fromtimestamp(file.stat().st_atime)
            if now - st_atime > datetime.timedelta(days=7):
                # delete files older than 7 days
                self.log.info(f'Remove {file} (older than 7 days)')
                file.unlink()

    @audio_files_cleaning_loop.before_loop
    async def before_audio_files_cleaning_loop(self):
        await self.bot.wait_until_ready()

        self.log.info('Start before_audio_files_cleaning_loop')

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

    @audio_files_cleaning_loop.error
    async def error_audio_files_cleaning_loop(self, e: Exception):
        self.log.error('Error during audio files cleaning loop', exc_info=e)
        self.audio_files_cleaning_loop.restart()

    @commands.Cog.listener('on_voice_state_update')
    async def voice_state_update(self, member, before, after):
        """Disconnect automatically when alone in a VoiceChannel.
        """
        for voice_client in self.bot.voice_clients:
            if len(voice_client.channel.members) == 1:
                jukebox = self.jukeboxes.get(voice_client.guild.id)
                if jukebox:
                    await jukebox.stop()
                    del self.jukeboxes[voice_client.guild.id]

    def get_jukebox(self, ctx: ApplicationContext) -> Jukebox:
        jukebox = self.jukeboxes.get(ctx.guild.id)
        if not jukebox:
            jukebox = Jukebox(ctx)
            self.jukeboxes[ctx.guild.id] = jukebox

        jukebox.start()
        return jukebox

    @commands.slash_command(name='download')
    async def download(self, ctx: ApplicationContext):
        return await ctx.respond('Not implemented')

    async def connect_to_author_voice_channel(self, ctx: ApplicationContext):
        """Joins the user voice channel if bot is not already playing in
        another voice channel.

        Args:
            ctx (discord.ApplicationContext)

        Raises:
            NotConnectedToVoiceChannelError: if author not connected to
                any voice channel.
        """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                raise NotConnectedToVoiceChannelError

    @commands.slash_command(name='join')
    async def join(self, ctx: ApplicationContext):
        """Joins the user voice channel.
        """
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            await ctx.respond('Connected', ephemeral=True)
        else:
            await ctx.respond(
                'You are not connected to a voice channel!',
                ephemeral=True
            )

    @commands.slash_command(name='play')
    async def play(self, ctx: ApplicationContext, *, query):
        """Plays a file from the local filesystem.
        """
        await ctx.defer()

        try:
            await self.connect_to_author_voice_channel(ctx)
        except NotConnectedToVoiceChannelError:
            return await ctx.respond(
                'You are not connected to a voice channel!',
                ephemeral=True
            )

        jukebox = self.get_jukebox(ctx)

        if jukebox.voice_client is None:
            # reattach the voice client if needed
            jukebox.voice_client = ctx.voice_client

        try:
            await self.connect_to_author_voice_channel(ctx)
        except NotConnectedToVoiceChannelError:
            return await ctx.respond(
                'You are not connected to a voice channel!',
                ephemeral=True
            )

        filename = self.music_dir / query

        if not filename.is_file():
            self.log.warning(
                f'User {ctx.author.name} ({ctx.author.id}) asked for '
                f'{filename}: no such file'
            )
            return await ctx.respond(f'{query}: no such file')

        await jukebox.songs.put(Song(ctx, filename))

        await ctx.respond(f'Added **{query}** to the queue')

    @commands.slash_command(name='yt')
    async def yt(self, ctx: ApplicationContext, *, query):
        """Plays from a query (almost anything youtube_dl supports).
        """
        await ctx.defer()

        try:
            await self.connect_to_author_voice_channel(ctx)
        except NotConnectedToVoiceChannelError:
            return await ctx.respond(
                'You are not connected to a voice channel!',
                ephemeral=True
            )

        jukebox = self.get_jukebox(ctx)

        if jukebox.voice_client is None:
            # reattach the voice client if needed
            jukebox.voice_client = ctx.voice_client

        data = await self.bot.loop.run_in_executor(
            executor=None,
            func=lambda: self.ytdl.extract_info(query, download=True)
        )

        if 'entries' in data:
            # Takes the first item from a playlist
            data = data['entries'][0]

        filename = self.ytdl.prepare_filename(data)

        await jukebox.songs.put(Song(
            ctx=ctx,
            source=filename,
            duration=data.get('duration'),
            url=data.get('url'),
            title=data.get('title'),
            thumbnail=data.get('thumbnail')
        ))

        await ctx.respond(f'Added **{data.get("title")}** to the queue')

    @commands.slash_command(name='pause')
    async def pause(self, ctx: ApplicationContext):
        """Toggle pause.
        """
        if not ctx.voice_client.is_connected():
            # voice client not connected
            return await ctx.respond(
                'Not connected to a voice chanel!',
                ephemeral=True
            )

        if not ctx.voice_client.is_playing():
            # nothing's playing
            return await ctx.respond(
                'Not playing anything!',
                ephemeral=True
            )

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            return await ctx.respond('Resume music', ephemeral=True)
        else:
            ctx.voice_client.pause()
            return await ctx.respond('Pause music', ephemeral=True)

    @commands.slash_command(name='quit')
    async def quit(self, ctx: ApplicationContext):
        """Stops and disconnects the bot from voice.
        """
        jukebox = self.get_jukebox(ctx)
        await jukebox.stop()
        del self.jukeboxes[ctx.guild.id]

        await ctx.respond('Disconnected', ephemeral=True)
