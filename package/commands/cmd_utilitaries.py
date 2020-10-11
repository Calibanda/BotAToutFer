# Utilitaries command for BotAToutFer
import os
import random
import json
import aiohttp

from discord.ext import commands

import const

class Utilitaire(commands.Cog):
    def __init__(self, bot, logger, bot_channel_id):
        self.bot = bot
        self.logger = logger
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="news", help="Donne le lien d'un ou plusieurs articles de presse du jour (par défaut 1).") # https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-web-request
    async def news(self, ctx, number_tiles: int=1):
        if str(ctx.channel.id) == self.bot_channel_id:

            async with aiohttp.ClientSession() as session:
                self.logger.warning(f"Asking for the local news")
                async with session.get(f"http://newsapi.org/v2/top-headlines?country=fr&apiKey={const.NEWS_TOKEN}") as r: # Retreve last news
                    if r.status == 200:
                        news = await r.json()

                        old_news = []

                        if os.path.isfile(const.LAST_NEWS_URL_PATH):
                            with open(const.LAST_NEWS_URL_PATH, "r") as f:
                                try:
                                    old_news = json.load(f) # We try to load the news who have already been displayed by the bot
                                except Exception:
                                    pass

                        today_news = [ article["url"] for article in news["articles"] if article["url"] not in old_news ] # We retreve all the url that hasn't been already displayed
                        news_to_display = today_news[:number_tiles] # We keep at most the number of articles asked from the user

                        for news in news_to_display:
                            await ctx.send(news)

                        old_news = old_news + news_to_display # We add the just displayed news to the old ones

                        with open(const.LAST_NEWS_URL_PATH, "w") as f:
                            json.dump(old_news[-25:], f, indent=4) # We store the 25 most recent displayed articles in a json file


    @commands.command(name="meteo", help="Donne la météo (d'une ville au hasard dans le monde).") # https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-web-request
    async def meteo(self, ctx):
        if str(ctx.channel.id) == self.bot_channel_id:

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
