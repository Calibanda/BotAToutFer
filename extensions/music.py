# Music commands for BotÀToutFer
import os
import time
import datetime
import asyncio
from urllib.parse import urlparse
import random
from pathlib import Path

import discord
from discord.ext import commands
import youtube_dl


# TODO: For auto disconnection: see discord.on_voice_state_update(member, before, after)

def setup(bot):
    bot.add_cog(Music(bot))


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.queue = {}
        self.queue_position = {}

        self.MUSIC_DIR = os.path.join(Path.home(), 'Music')
        self.RPG_COMBAT_DIR = os.path.join(MUSIC_DIR, "RPG_Combat")
        self.RPG_EXPLORATION_DIR = os.path.join(MUSIC_DIR, "RPG_Exploration")
        self.RPG_TAVERN_DIR = os.path.join(MUSIC_DIR, "RPG_TAVERN")


    @commands.command(name="join", help="Connecte le bot dans un salon vocal")
    async def join(self, ctx, *, channel: discord.VoiceChannel=None):
        """Joins a voice channel"""

        if not channel:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
            else:
                return await ctx.send("Mais où veux tu que je me connecte ??")

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    @commands.command(name="play", help="Joue la playlist ou le lien précisé en paramètre", aliases=['p'])
    async def play(self, ctx, *, query: str=""):
        """Plays a file from the local filesystem"""

        if query == "combat":
            await self.play_rpg_music(ctx, self.RPG_COMBAT_DIR)
        elif query == "exploration":
            await self.play_rpg_music(ctx, self.RPG_EXPLORATION_DIR)
        elif query == "tavern":
            await self.play_rpg_music(ctx, self.RPG_TAVERN_DIR)
        elif urlparse(query).netloc:

            try:
                async with ctx.typing():
                    player = await YTDLSource.from_url(query, loop=self.bot.loop, stream=False)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                await ctx.send(f'Now playing: {player.title}')
            except Exception as e:
                self.bot.log.exception(f"Audio exception in this channel: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
                await ctx.send(f"Something went wrong")

        else:
            response = "Je ne comprend pas ce que tu veux que je joue..."
            await ctx.send(response)


    async def play_rpg_music(self, ctx, directory):
        try:
            # Get the list of all files in directory tree at given path
            list_of_files = []
            for (dirpath, dirnames, filenames) in os.walk(directory):
                list_of_files += [ os.path.join(dirpath, file_name) for file_name in filenames ]
            random.shuffle(list_of_files)
        except Exception as e:
            self.bot.log.exception(f"Audio exception in this channel: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)

        if not list_of_files:
            response = "No such file or directory"
            return await ctx.send(response)

        self.queue[ctx.voice_client] = list_of_files
        self.queue_position[ctx.voice_client] = 0
        await self.play_queue(ctx)


    async def play_queue(self, ctx):
        try:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.queue[ctx.voice_client][self.queue_position[ctx.voice_client]]))
            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(ctx.send('Player error: %s' % e), self.bot.loop) if e else self.next_audio(ctx))
            music_title = self.queue[ctx.voice_client][self.queue_position[ctx.voice_client]]
            music_title = os.path.split(music_title)[-1]
            music_title = os.path.splitext(music_title)[0]
            await ctx.send(f"Now playing: {music_title}")

        except Exception as e:
            self.bot.log.exception(f"Audio exception in this channel: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            await ctx.send(f"Something went wrong")


    def next_audio(self, ctx):
        if self.queue_position[ctx.voice_client] < len(self.queue[ctx.voice_client]):
            self.queue_position[ctx.voice_client] += 1
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.queue[ctx.voice_client][self.queue_position[ctx.voice_client]]))
            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(ctx.send('Player error: %s' % e), self.bot.loop) if e else self.next_audio(ctx))
            music_title = self.queue[ctx.voice_client][self.queue_position[ctx.voice_client]]
            music_title = os.path.split(music_title)[-1]
            music_title = os.path.splitext(music_title)[0]
            asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing: {music_title}"), self.bot.loop)
        else:
            asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), self.bot.loop)


    @commands.command(name="next", help="Joue le morceau suivant")
    async def next(self, ctx):
        if self.queue_position[ctx.voice_client] < len(self.queue[ctx.voice_client]):
            self.queue_position[ctx.voice_client] += 1
            ctx.voice_client.stop()
            await self.play_queue(ctx)
        else:
            await ctx.send("No next track")


    # @commands.command(name="previous", help="Joue le morceau précédent")
    # async def previous(self, ctx):
    #     if self.queue_position[ctx.voice_client] > 0:
    #         self.queue_position[ctx.voice_client] -= 1
    #         ctx.voice_client.stop()
    #         await self.play_queue(ctx)
    #     else:
    #         await ctx.send("No previous track")


    # @commands.command()
    # async def yt(self, ctx, *, url):
    #     """Plays from a url (almost anything youtube_dl supports)"""

    #     async with ctx.typing():
    #         player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #         ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    #     await ctx.send('Now playing: {}'.format(player.title))


    @commands.command(name="stream", help="Stream de la musique depuis un lien", aliases=['s'])
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.send('Now playing: {}'.format(player.title))
        except Exception as e:
            self.bot.log.exception(f"Audio exception in this channel: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            await ctx.send(f"Something went wrong")


    # @commands.command(name="volume", help="Change le volume sonore du bot")
    # async def volume(self, ctx, volume: int):
    #     """Changes the player's volume"""

    #     if ctx.voice_client is None:
    #         return await ctx.send("Not connected to a voice channel.")

    #     ctx.voice_client.source.volume = volume / 100
    #     await ctx.send("Changed volume to {}%".format(volume))


    @commands.command(name="quit", help="Déconnecte le bot du salon vocal")
    async def quit(self, ctx):
        """Stops and disconnects the bot from voice"""
        self.queue_position[ctx.voice_client] = 0
        self.queue[ctx.voice_client] = []
        await ctx.voice_client.disconnect()


    @play.before_invoke
    # @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                # raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


    @commands.command(name="name", help="Demande au bot de dire son nom")
    async def name(self, ctx):
        await speak("Je suis le bot a tout faire")
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(os.path.join(self.bot.SCRIPT_DIR, "package", "audio", "audio.mp3")))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)


    @commands.command(name="hello", help="Demande au bot de dire 'Hello World'")
    async def hello(self, ctx):
        await speak("Hello world!")
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(os.path.join(self.bot.SCRIPT_DIR, "package", "audio", "audio.mp3")))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
