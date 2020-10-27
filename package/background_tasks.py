import secrets
import aiohttp
import datetime

from discord.ext import tasks, commands

import const

class Tasks(commands.Cog):
    def __init__(self, bot, cat_channels, logger):
        self.bot = bot
        self.cat_channels = cat_channels
        self.logger = logger
        self.cat.start()

    def cog_unload(self):
        self.cat.cancel()

    @tasks.loop(minutes=5.0)
    async def cat(self):
        for channel in self.cat_channels:
            if secrets.randbelow(192) < 2 and datetime.datetime.now().hour in range(7, 23):
                async with aiohttp.ClientSession() as session:
                    self.logger.warning(f"Asking for a cat pic")
                    async with session.get(f"https://api.thecatapi.com/v1/images/search?api_key={const.CAT_TOKEN}") as r: # Retreve a cat json
                        if r.status == 200:
                            cat = await r.json()
                            message = cat[0]["url"]

                            await channel.send(message)

    @cat.before_loop
    async def before_cat(self):
        await self.bot.wait_until_ready()