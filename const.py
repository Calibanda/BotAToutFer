# const.py
import os
import datetime

from dotenv import load_dotenv

SCRIPT_DIR, SCRIPT_FILENAME = os.path.split(os.path.abspath(__file__))

load_dotenv() # Loads tokens form env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
NEWS_TOKEN = os.getenv("NEWS_TOKEN")

BOT_CHANNEL = "bot-test"
BOT_CHANNEL_ID = "763426416167485481"

LOG_DIR = os.path.join(SCRIPT_DIR, "logs") # The directory containing logs
LOG_FILE_PATH = os.path.join(LOG_DIR, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log") # Absolute path of the new log file

LAST_NEWS_URL_PATH = os.path.join(SCRIPT_DIR, "package", "last_news_url.json")

BOT_DESCRIPTION = "BotAToutFer, le bot qui fait tout, même le café !"

CURSE_LIST = [
    {"curse_word": "merde", "traduction": "merle"},
    {"curse_word": "putain", "traduction": "mutin"},
    {"curse_word": "connard", "traduction": "canard"},

    {"curse_word": "fuck", "traduction": "fork"},
    {"curse_word": "shit", "traduction": "shirt"},
    {"curse_word": "bitch", "traduction": "bench"},
    {"curse_word": "asshole", "traduction": "ash-hole"},
    {"curse_word": "ass", "traduction": "ash"},
    {"curse_word": "cock", "traduction": "cork"},
    {"curse_word": "dick", "traduction": "deck"},

]
