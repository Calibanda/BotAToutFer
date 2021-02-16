# const.py
import os
import datetime
import json
from pathlib import Path

from dotenv import load_dotenv


SCRIPT_DIR, SCRIPT_FILENAME = os.path.split(os.path.abspath(__file__)) # Retreve the directory path of the script

load_dotenv() # Loads tokens form env
TOKEN = os.getenv("DISCORD_TOKEN")
#GUILD = os.getenv("DISCORD_GUILD")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
NEWS_TOKEN = os.getenv("NEWS_TOKEN")
CAT_TOKEN = os.getenv("CAT_TOKEN")
#ANTOINE_TAG = int(os.getenv("ANTOINE_TAG"))
OWNER_ID = int(os.getenv("OWNER_ID"))
COFFEE_URL = os.getenv("COFFEE_URL")
COFFEE_PASSWORD = os.getenv("COFFEE_PASSWORD")
DICOLINK_TOKEN = os.getenv("DICOLINK_TOKEN")

LOG_DIR = os.path.join(SCRIPT_DIR, "logs") # The directory containing logs
LOG_FILE_PATH = os.path.join(LOG_DIR, datetime.datetime.now().strftime("%Y-%m-%d") + ".log") # Absolute path of the new log file

BOT_DESCRIPTION = "BotAToutFer, le bot qui fait tout, même le café !" # The description of the bot
BOT_ACTIVITY = "!help" # The Discord activity of the bot

MUSIC_DIR = os.path.join(Path.home(), "Music") # The user music directory
RPG_COMBAT_DIR = os.path.join(MUSIC_DIR, "RPG_Combat")
RPG_EXPLORATION_DIR = os.path.join(MUSIC_DIR, "RPG_Exploration")
RPG_TAVERN_DIR = os.path.join(MUSIC_DIR, "RPG_TAVERN")
