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
                    self.cat_authorized_channels.append(self.bot.get_channel(int(channel_id)))
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error("cat_channels.json file not found: ", exc_info=e)

        self.CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
        self.CAT_API_PARAMS = {"api_key": self.bot.CAT_TOKEN}
        self.RED_PANDA_URL = "https://some-random-api.ml/img/red_panda"
        self.OTTER_URL = f"https://www.reddit.com/r/Otters/hot.json"
        self.OTTER_PARAMS = {"limit": "50", "t": "day"}

        self.cat.start()

    def cog_unload(self):
        self.cat.cancel()

    @tasks.loop(minutes=6.0)
    async def cat(self):
        for channel in self.cat_authorized_channels:
            if random.randrange(180) < 1 and datetime.datetime.now().hour in range(7, 23):
                # Statistically send 1 message per day
                # (one chance on 160 every 6 minutes between 7AM and 11PM)
                try:
                    async with aiohttp.ClientSession() as session:

                        choice = random.choice(["cat", "cat", "cat", "otter", "red panda"])
                        if choice == "cat":
                            self.bot.log.warning(f"Asking for a cat pic in this channel: {channel.guild}, #{channel.name} ({channel.id})")
                            async with session.get(url=self.CAT_API_URL, params=self.CAT_API_PARAMS) as r:
                                # Retrieve a cat json
                                if r.status == 200:
                                    cat = await r.json()
                                    message = cat[0]["url"]

                        elif choice == "red panda":
                            self.bot.log.warning(f"Asking a red fox pic in this channel: {channel.guild}, #{channel.name} ({channel.id})")
                            async with session.get(url=self.RED_PANDA_URL) as r:
                                # Retrieve a red fox json
                                if r.status == 200:
                                    red_panda = await r.json()
                                    message = red_panda["link"]

                        else:
                            self.bot.log.warning(f"Asking an otter pic in this channel: {channel.guild}, #{channel.name} ({channel.id})")
                            async with session.get(url=self.OTTER_URL, params=self.OTTER_PARAMS) as r:
                                if r.status == 200:
                                    otter = await r.json()

                                    urls = []
                                    for post in otter["data"]["children"]:
                                        try:
                                            hint = post["data"]["post_hint"]
                                            post_url = post["data"]["url"]
                                        except Exception as e:
                                            pass
                                        else:
                                            if post_url.startswith("https://i.redd.it/") and hint == "image":
                                                urls.append(post["data"]["url"])

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
            with open(self.CAT_CHANNELS_PATH, "r") as f:
                # Loads authorized channels id from json
                cat_json = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            cat_json = {}

        if str(ctx.channel.id) in cat_json:
            # Channel id is in json so we remove it
            del cat_json[str(ctx.channel.id)]
            response = "Disable cute animal pictures in this channel"
        else:  # Channel id is NOT in json so we add it
            cat_json[str(ctx.channel.id)] = f"{ctx.channel.guild.name} > {ctx.channel.name}"
            response = "Enable cute animal pictures in this channel"

        with open(self.CAT_CHANNELS_PATH, "w", encoding="utf8") as f:
            json.dump(cat_json, f, indent=4, ensure_ascii=False)

        self.cat_authorized_channels = []  # We reload cat channels
        for channel_id in cat_json.keys():
            self.cat_authorized_channels.append(self.bot.get_channel(int(channel_id)))

        await ctx.send(response)
