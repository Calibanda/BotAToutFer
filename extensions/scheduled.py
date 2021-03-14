# Scheduled tasks for for BotÀToutFer
import random
import aiohttp
import datetime
import os
import json

import asyncio
from discord.ext import commands


def setup(bot):
    bot.add_cog(Scheduled(bot))
    bot.loop.create_task(Scheduled(bot).daily_task())


class Scheduled(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden_cog = True
        self.CAT_CHANNELS_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "cat_channels.json"
        )
        self.cat_authorized_channels = []
        try:
            with open(self.CAT_CHANNELS_PATH, "r") as f:
                # Loads authorized channels id from json
                for channel_id in json.load(f).keys():
                    self.cat_authorized_channels.append(
                        self.bot.get_channel(int(channel_id))
                    )
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error(f"Caught exception:", exc_info=e)

    async def daily_task(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            alarm = datetime.datetime.now().replace(
                hour=8,
                minute=0,
                second=0,
                microsecond=0
            )
            delta = (alarm - datetime.datetime.now()).total_seconds()
            if delta < 0:  # 8AM is passed today
                alarm = alarm + datetime.timedelta(days=1)
                delta = (alarm - datetime.datetime.now()).total_seconds()
            await asyncio.sleep(delta)
            self.bot.log.waring("It's 8 AM: " + str(datetime.datetime.now()))
