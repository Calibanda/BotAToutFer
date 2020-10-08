# main.py
import os
import random
import logging
import datetime
import re
import json
import requests
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

SCRIPT_DIR, SCRIPT_FILENAME = os.path.split(os.path.abspath(__file__))

load_dotenv() # Loads tokens form env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
BOT_CHANNEL = "bot-test"

LOG_DIR = os.path.join(SCRIPT_DIR, "logs") # The directory containing logs
LOG_FILE_PATH = os.path.join(LOG_DIR, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log") # Absolute path of the new log file

if not os.path.exists(LOG_DIR): # If the logs directory does not exist, we create it
    os.makedirs(LOG_DIR)

# Setting up the logging system
logger = logging.getLogger("discord")
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename=LOG_FILE_PATH, encoding="utf-8", mode="a")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
logger.addHandler(handler)

BOT_DESCRIPTION = "BotAToutFer, le bot qui fait tout, même le café !"


bot = commands.Bot(command_prefix="!", description=BOT_DESCRIPTION)


@bot.event
async def on_ready():
    """When the bot is connected to the guild, print guild informations"""
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f"{bot.user} is connected to the following guild:\n{guild.name} (id: {guild.id})")
    logger.warning(f"{bot.user} is connected to the following guild: {guild.name} (id: {guild.id})")

    bot_channel = discord.utils.get(guild.channels, name=BOT_CHANNEL)
    # await bot_channel.send("Salut, je suis le BotAToutFer ! Je suis réveillé donc vous pouvez m'utiliser :smirk:")


@bot.event
async def on_command_error(ctx, error):
    """When a command error occures displays the reason in the gild chat"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("Nope, t'as pas le droit :P")
    else:
        await ctx.send("https://tenor.com/view/of-its-not-false-its-true-agree-gif-16911578")


@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(event, exc_info=args[0])
    raise


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

    if "je suis " in message.content.lower():
        i_am = re.split(r"je suis ", message.content, 1, flags=re.IGNORECASE)[-1]
        response = f"Salut *{i_am}*, moi c'est le {bot.user.mention}"
        await message.channel.send(response)

@bot.command(name="ping", help="Responds pong.")
async def ping(ctx):
    response = "pong"
    await ctx.send(response)


@bot.command(name="99", help="Responds a B99 quote.")
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        "I'm the human form of the :100: emoji.",
        "Bingpot!",
        "Cool. Cool cool cool cool cool cool cool, no doubt no doubt no doubt no doubt.",
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name="roll_dice", help="Simulates rolling dice.")
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [ str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice) ]
    response = ", ".join(dice)
    await ctx.send(response)


@bot.command(name="green", help="Sends a tree.")
@commands.has_role("Design4green")
async def green(ctx):
    response = ":evergreen_tree:"
    await ctx.send(response)


@bot.command(name="coffee", help="Send a coffee.")
async def green(ctx):
    response = ":coffee:"
    await ctx.send(response)


@bot.command(name="tea", help="Send a tea.")
async def green(ctx):
    response = ":tea:"
    await ctx.send(response)


@bot.command(name="meteo", help="Gives the weather (of a random city in the world).")
async def meteo(ctx):
    with open(os.path.join(SCRIPT_DIR, "package", "list_city_id.json"), "r") as f:
        list_city_id = json.load(f)
    
    random_city = random.choice(list_city_id)
    weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={random_city}&appid=d9261c180caef00c5a538827a0b32612&units=metric&lang=fr").json()
    logger.warning(f"Asking for the weather of the city number {random_city}")
    w_description = weather["weather"][0]["description"]
    w_temp = round(weather["main"]["temp"], 1)
    response = f"Actuellement {w_description}, il fait {w_temp} °C (quelque part dans le monde :earth_africa:)."
    await ctx.send(response)


bot.run(TOKEN)
