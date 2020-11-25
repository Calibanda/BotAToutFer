import secrets
import aiohttp
import datetime

from discord.ext import tasks, commands

import const

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cat.start()
        self.hidden_cog = True

    def cog_unload(self):
        self.cat.cancel()

    @tasks.loop(minutes=5.0)
    async def cat(self):
        for channel in self.bot.autorized_channel:
            if secrets.randbelow(192) < 2 and datetime.datetime.now().hour in range(7, 23):
                try:
                    async with aiohttp.ClientSession() as session:
                        self.bot.log.warning(f"Asking for a cat pic")
                        async with session.get(f"https://api.thecatapi.com/v1/images/search?api_key={const.CAT_TOKEN}") as r: # Retreve a cat json
                            if r.status == 200:
                                cat = await r.json()
                                message = cat[0]["url"]

                                await channel.send(message)
                except Exception as e:
                    self.bot.log.exception(f"Unable to send a cat in this channel: {channel.guild}, #{channel.name} ({channel.id})")

    @cat.before_loop
    async def before_cat(self):
        await self.bot.wait_until_ready()
