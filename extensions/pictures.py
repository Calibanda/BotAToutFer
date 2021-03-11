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

    def cog_unload(self):
        self.cat.cancel()

    @tasks.loop(minutes=6.0)
    async def cat(self):
        for channel in self.cat_authorized_channels:
            if (random.randrange(180) < 1
                    and datetime.datetime.now().hour in range(7, 23)):
                # Statistically send 1 message per day
                # (one chance on 160 every 6 minutes between 7AM and 11PM)
                try:
                    async with aiohttp.ClientSession() as session:

                        choice = random.choice(
                            ["cat", "cat", "cat", "otter", "red panda"]
                        )
                        if choice == "cat":
                            self.bot.log.warning(
                                (
                                    "Asking for a cat pic in this channel: "
                                    + f"{channel.guild}, "
                                    + f"#{channel.name} ({channel.id})"
                                )
                            )
                            url = (
                                "https://api.thecatapi.com/v1/images/search?"
                                + f"api_key={self.bot.CAT_TOKEN}"
                            )
                            async with session.get(url) as r:
                                # Retrieve a cat json
                                if r.status == 200:
                                    cat = await r.json()
                                    message = cat[0]["url"]

                        elif choice == "red panda":
                            self.bot.log.warning(
                                (
                                    "Asking a red fox pic in this channel: "
                                    + f"{channel.guild}, "
                                    + f"#{channel.name} ({channel.id})"
                                )
                            )
                            url = "https://some-random-api.ml/img/red_panda"
                            async with session.get(url) as r:
                                # Retrieve a red fox json
                                if r.status == 200:
                                    red_panda = await r.json()
                                    message = red_panda["link"]

                        else:
                            subreddit = "Otters"
                            limit = 50
                            timeframe = "day"
                            listing = "hot"

                            self.bot.log.warning(
                                (
                                    "Asking an otter pic in this channel: "
                                    + f"{channel.guild}, "
                                    + f"#{channel.name} ({channel.id})"
                                )
                            )
                            url = (
                                f"https://www.reddit.com/r/{subreddit}/"
                                + f"{listing}.json?"
                                + f"limit={limit}&t={timeframe}"
                            )
                            async with session.get(url) as r:
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
                                            if (post_url.startswith(
                                                    "https://i.redd.it/")
                                                    and hint == "image"):
                                                urls.append(
                                                    post["data"]["url"]
                                                )

                                    random.shuffle(urls)
                                    message = urls[0]

                        await channel.send(message)

                except Exception as e:
                    self.bot.log.exception(
                        (
                            "Unable to send a cute picture in this channel: "
                            + f"{channel.guild}, "
                            + f"#{channel.name} ({channel.id})"
                        ),
                        exc_info=e
                    )

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
            cat_json[str(ctx.channel.id)] = (
                f"{ctx.channel.guild.name} > {ctx.channel.name}"
            )
            response = "Enable cute animal pictures in this channel"

        with open(self.CAT_CHANNELS_PATH, "w", encoding='utf8') as f:
            json.dump(cat_json, f, indent=4, ensure_ascii=False)

        self.cat_authorized_channels = []  # We reload cat channels
        for channel_id in cat_json.keys():
            self.cat_authorized_channels.append(
                self.bot.get_channel(int(channel_id))
            )

        await ctx.send(response)
