# meteo command for BotAToutFer
import os
import random
import json
import aiohttp

from discord.ext import commands

import const

class Weather(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger
        self._last_member = None

    @commands.command(name="meteo", help="Gives the weather (of a random city in the world).") # https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-web-request
    async def meteo(self, ctx):

        with open(os.path.join(const.SCRIPT_DIR, "package", "list_city_id.json"), "r") as f:
            list_city_id = json.load(f)
        
        random_city = random.choice(list_city_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.openweathermap.org/data/2.5/weather?id={random_city}&appid={const.WEATHER_TOKEN}&units=metric&lang=fr") as r:

                if r.status == 200:
                    weather = await r.json()

                    #weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={random_city}&appid={WEATHER_TOKEN}&units=metric&lang=fr").json()
                    self.logger.warning(f"Asking for the weather of the city number {random_city}")
                    w_description = weather["weather"][0]["description"]
                    w_temp = round(weather["main"]["temp"], 1)
                    response = f"Actuellement {w_description}, il fait {w_temp} °C (quelque part dans le monde :earth_africa:)."
                    await ctx.send(response)
