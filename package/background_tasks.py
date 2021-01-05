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


    @tasks.loop(minutes=6.0)
    async def cat(self):
        for channel in self.bot.autorized_channel:
            if secrets.randbelow(160) < 1 and datetime.datetime.now().hour in range(7, 23): # Statisticly send 1 message per day (one chance on 160 every 6 minutes between 7AM and 11PM)
                try:
                    async with aiohttp.ClientSession() as session:

                        if secrets.choice(["cat", "red panda"]) == "cat":
                            self.bot.log.warning(f"Asking for a cat pic")
                            async with session.get(f"https://api.thecatapi.com/v1/images/search?api_key={const.CAT_TOKEN}") as r: # Retreve a cat json
                                if r.status == 200:
                                    cat = await r.json()
                                    message = cat[0]["url"]

                        else:
                            self.bot.log.warning(f"Asking a red fox pic")
                            async with session.get("https://some-random-api.ml/img/red_panda") as r: # Retreve a red fox json
                                if r.status == 200:
                                    red_panda = await r.json()
                                    message = red_panda["link"]

                        await channel.send(message)

                except Exception as e:
                    self.bot.log.exception(f"Unable to send a cat in this channel: {channel.guild}, #{channel.name} ({channel.id})")


    @cat.before_loop
    async def before_cat(self):
        await self.bot.wait_until_ready()
