# main.py
from bot_init import bot_init


if __name__ == "__main__":
    bot = bot_init()
    bot.run(bot.TOKEN)
