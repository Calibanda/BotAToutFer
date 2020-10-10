# news command for BotAToutFer
import os
import json
import aiohttp

from discord.ext import commands

import const

class News(commands.Cog):
    def __init__(self, bot, logger, bot_channel_id):
        self.bot = bot
        self.logger = logger
        self.bot_channel_id = bot_channel_id
        self._last_member = None

    @commands.command(name="news", help="Gives the news headlines.") # https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-web-request
    async def news(self, ctx, number_tiles: int=1):
        if str(ctx.channel.id) == self.bot_channel_id:

            async with aiohttp.ClientSession() as session:
                self.logger.warning(f"Asking for the local news")
                async with session.get(f"http://newsapi.org/v2/top-headlines?country=fr&apiKey={const.NEWS_TOKEN}") as r:
                    if r.status == 200:
                        news = await r.json()

                        old_news = []

                        if os.path.isfile(const.LAST_NEWS_URL_PATH):
                            with open(const.LAST_NEWS_URL_PATH, "r") as f:
                                try:
                                    old_news = json.load(f)
                                except Exception:
                                    pass

                        today_news = [ article["url"] for article in news["articles"] if article["url"] not in old_news ]
                        news_to_display = today_news[:number_tiles]

                        for news in news_to_display:
                            await ctx.send(news)

                        old_news = old_news + news_to_display

                        with open(const.LAST_NEWS_URL_PATH, "w") as f:
                            json.dump(old_news[:50], f, indent=4)
