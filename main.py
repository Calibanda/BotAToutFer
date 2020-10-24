# main.py

from bot_init import bot_init
import const


if __name__ == "__main__":
    bot = bot_init()
    bot.run(const.TOKEN) # See help here for the loggout message
