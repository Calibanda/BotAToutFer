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

with open(os.path.join(SCRIPT_DIR, "package", "channels.json"), "r") as f: # Loads authorized channels id from json
    AUTORIZED_CHANNELS = [ int(channel_id) for channel_id in json.load(f).keys() ]

LOG_DIR = os.path.join(SCRIPT_DIR, "logs") # The directory containing logs
LOG_FILE_PATH = os.path.join(LOG_DIR, datetime.datetime.now().strftime("%Y-%m-%d") + ".log") # Absolute path of the new log file

LAST_NEWS_URL_PATH = os.path.join(SCRIPT_DIR, "package", "last_news_url.json") # The path of the json file containing the lastest retrived news

BOT_DESCRIPTION = "BotAToutFer, le bot qui fait tout, même le café !" # The description of the bot
BOT_ACTIVITY = "!help" # The Discord activity of the bot

MUSIC_DIR = os.path.join(Path.home(), "Music") # The user music directory
RPG_COMBAT_DIR = os.path.join(MUSIC_DIR, "RPG_Combat")
RPG_EXPLORATION_DIR = os.path.join(MUSIC_DIR, "RPG_Exploration")
RPG_TAVERN_DIR = os.path.join(MUSIC_DIR, "RPG_TAVERN")

CURSE_LIST = [ # The list of cursed words
    {"curse_word": "merde", "traduction": "merle"},
    {"curse_word": "putain", "traduction": "mutin"},
    {"curse_word": "connard", "traduction": "canard"},
    {"curse_word": "connarde", "traduction": "canarde"},
    {"curse_word": "connasse", "traduction": "godasse"},
    {"curse_word": "pute", "traduction": "butte"},
    {"curse_word": "bordel", "traduction": "bordé"},
    {"curse_word": "foutre", "traduction": "floute"},
    #{"curse_word": "poufiace", "traduction": ""},
    {"curse_word": "enculé", "traduction": "granulé"},

    {"curse_word": "fuck", "traduction": "fork"},
    {"curse_word": "fucking", "traduction": "forking"},
    {"curse_word": "fucker", "traduction": "forker"},
    {"curse_word": "shit", "traduction": "shirt"},
    {"curse_word": "bitch", "traduction": "bench"},
    {"curse_word": "asshole", "traduction": "ash-hole"},
    {"curse_word": "ass", "traduction": "ash"},
    {"curse_word": "cock", "traduction": "cork"},
    {"curse_word": "dick", "traduction": "deck"},

]

SCRABBLE_DICTIONARY_PATH = os.path.join(SCRIPT_DIR, "package", "ODS7.txt") # Path of the french scrabble dictionary

FRENCH_SCRABBLE_VALUES = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8,
                          "K": 10, "L": 1, "M": 2, "N": 1, "O": 1, "P": 3, "Q": 8, "R": 1, "S": 1, "T": 1,
                          "U": 1, "V": 4, "W": 10, "X": 10, "Y": 10, "Z": 10}

LIST_JE_SUIS = [
    "je suis ",
    "j'suis ",
    "chuis ",
    "chui ",
    "j'sui ",
    "j suis ",
    "j sui ",
]

with open(os.path.join(SCRIPT_DIR, "package", "dico_marseillais.json"), "r") as f:
    DICO_MARSEILLAIS = json.load(f)
