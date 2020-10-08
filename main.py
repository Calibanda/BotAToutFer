# main.py
import os
import random
import logging
import datetime
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

SCRIPT_DIR, SCRIPT_FILENAME = os.path.split(os.path.abspath(__file__))

load_dotenv() # Loads tokens form env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

LOG_DIR = os.path.join(SCRIPT_DIR, "logs") # The directory containing logs
LOG_FILE_PATH = os.path.join(LOG_DIR, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log") # Absolute path of the new log file

if not os.path.exists(LOG_DIR): # If the logs directory does not exist, we create it
    os.makedirs(LOG_DIR)

# Setting up the logging system
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
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


@bot.event
async def on_command_error(ctx, error):
    """When a command error occures displays the reason in the gild chat"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("Nope, t'as pas le droit :P")
    else:
        await ctx.send("https://tenor.com/view/of-its-not-false-its-true-agree-gif-16911578")


#@bot.event
#async def on_error(event, *args, **kwargs):
#    with open('err.log', 'a') as f:
#        if event == 'on_message':
#            f.write(f'Unhandled message: {args[0]}\n')
#        else:
#            raise


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
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(", ".join(dice))


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


bot.run(TOKEN)
