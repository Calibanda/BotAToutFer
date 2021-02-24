# background pictures for for BotÀToutFer (send cute animals pictures)
import random
import aiohttp
import datetime
import os
import json

from discord.ext import tasks, commands


def setup(bot):
    bot.add_cog(Pictures(bot))


class Pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cat.start()
        self.hidden_cog = True
        self.CAT_CHANNELS_PATH = os.path.join(self.bot.SCRIPT_DIR, "package", "cat_channels.json")
        try:
            with open(self.CAT_CHANNELS_PATH, "r") as f: # Loads authorized channels id from json
                self.cat_authorized_channels = [ self.bot.get_channel(int(channel_id)) for channel_id in json.load(f).keys() ] # bot.get_channel(channel_id)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error(f"Catched exeption:", exc_info=e)
            self.cat_authorized_channels = []


    def cog_unload(self):
        self.cat.cancel()


    @tasks.loop(minutes=6.0)
    async def cat(self):
        for channel in self.cat_authorized_channels:
            if random.randrange(180) < 1 and datetime.datetime.now().hour in range(7, 23): # Statisticly send 1 message per day (one chance on 160 every 6 minutes between 7AM and 11PM)
                try:
                    async with aiohttp.ClientSession() as session:

                        choice = random.choice(["cat", "cat", "cat", "otter", "red panda"])
                        if choice == "cat":
                            self.bot.log.warning(f"Asking for a cat pic in this channel: {channel.guild}, #{channel.name} ({channel.id})")
                            async with session.get(f"https://api.thecatapi.com/v1/images/search?api_key={self.bot.CAT_TOKEN}") as r: # Retreve a cat json
                                if r.status == 200:
                                    cat = await r.json()
                                    message = cat[0]["url"]

                        elif choice == "red panda":
                            self.bot.log.warning(f"Asking a red fox pic in this channel: {channel.guild}, #{channel.name} ({channel.id})")
                            async with session.get("https://some-random-api.ml/img/red_panda") as r: # Retreve a red fox json
                                if r.status == 200:
                                    red_panda = await r.json()
                                    message = red_panda["link"]

                        else:
                            subreddit = "Otters"
                            limit = 50
                            timeframe = "day" #hour, day, week, month, year, all
                            listing = "hot" # controversial, best, hot, new, random, rising, top

                            self.bot.log.warning(f"Asking an otter pic in this channel: {channel.guild}, #{channel.name} ({channel.id})")
                            async with session.get(f"https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}") as r:
                                if r.status == 200:
                                    otter_data = await r.json()

                                    urls = []
                                    for post in otter_data["data"]["children"]:
                                        try:
                                            if post["data"]["post_hint"] == "image" and post["data"]["url"].startswith("https://i.redd.it/"):
                                                urls.append(post["data"]["url"])
                                        except Exception as e:
                                            pass

                                    random.shuffle(urls)
                                    message = urls[0]

                        await channel.send(message)

                except Exception as e:
                    self.bot.log.exception(f"Unable to send a cute picture in this channel: {channel.guild}, #{channel.name} ({channel.id})", exc_info=e)


    @cat.before_loop
    async def before_cat(self):
        await self.bot.wait_until_ready()

    @commands.command(name="pictures")
    @commands.is_owner()
    async def pictures(self, ctx):
        try:
            with open(self.CAT_CHANNELS_PATH, "r") as f: # Loads authorized channels id from json
                cat_json = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            cat_json = {}

        if str(ctx.channel.id) in cat_json: # Channel id is in json so we remove it
            del cat_json[str(ctx.channel.id)]
            response = "Disable cute animal pictures in this channel"
        else: # Channel id is NOT in json so we add it
            cat_json[str(ctx.channel.id)] = f"{ctx.channel.guild.name} > {ctx.channel.name}"
            response = "Enable cute animal pictures in this channel"

        with open(self.CAT_CHANNELS_PATH, "w", encoding='utf8') as f:
            json.dump(cat_json, f, indent=4, ensure_ascii=False)

        self.cat_authorized_channels = [ self.bot.get_channel(int(channel_id)) for channel_id in cat_json.keys() ] # We reload cat channels

        await ctx.send(response)
