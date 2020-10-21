# main.py
import re

import discord
from discord.ext import commands

import const
import set_logger

from package.commands.cmd_discussion import Discussion
from package.commands.cmd_drinks import Drinks
from package.commands.cmd_green import Green
from package.commands.cmd_help import Help
from package.commands.cmd_ping import Ping
from package.commands.cmd_quotes import Quotes
from package.commands.cmd_roll_dice import Roll_dice
from package.commands.cmd_says import Says
from package.commands.cmd_utilitaries import Utilitaire

logger = set_logger.init()

bot = commands.Bot(command_prefix="!", description=const.BOT_DESCRIPTION)
bot.remove_command('help')

bot.add_cog(Discussion(bot))
bot.add_cog(Drinks(bot))
bot.add_cog(Green(bot))
bot.add_cog(Help(bot))
bot.add_cog(Ping(bot))
bot.add_cog(Quotes(bot))
bot.add_cog(Roll_dice(bot))
bot.add_cog(Says(bot))
bot.add_cog(Utilitaire(bot, logger))


@bot.event
async def on_ready():
    """When the bot is connected to the guild, print guild informations"""
    guild = discord.utils.get(bot.guilds, name=const.GUILD)
    print(f"{bot.user} is connected to the following guild:\n{guild.name} (id: {guild.id})")
    logger.warning(f"{bot.user} is connected to the following guild: {guild.name} (id: {guild.id})")

    bot_channel = discord.utils.get(guild.channels, name=const.BOT_CHANNEL)
    # await bot_channel.send("Salut, je suis le BotAToutFer ! Je suis réveillé donc vous pouvez m'utiliser :smirk:")


@bot.event
async def on_command_error(ctx, error):
    """When a command error occures displays the reason in the gild chat"""
    logger.error(f"On command error: {repr(error)}")
    if str(ctx.channel.id) == const.BOT_CHANNEL_ID:
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("Nope, t'as pas le droit :P")
        else:
            await ctx.send("https://tenor.com/uqe8.gif") # Send a "C'est pas faux" gif


@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(event, exc_info=args[0])
    raise


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if str(message.channel) == const.BOT_CHANNEL and message.content.startswith("!"):
        await bot.process_commands(message)
        return

    if any(je_suis in message.content.lower() for je_suis in const.LIST_JE_SUIS):
        regex_je_suis = "(" + ")|(".join(const.LIST_JE_SUIS) + ")"
        i_am = re.split(regex_je_suis, message.content, 1, flags=re.IGNORECASE)[-1]
        response = f"Salut *{i_am}*, moi c'est le {bot.user.mention}"
        await message.channel.send(response)

    if any(re.match(r"(?<![:\w*:])" + curse_dict["curse_word"], message.content.lower()) + " " for curse_dict in const.CURSE_LIST):
        response = f"{message.author.mention} : {message.content} "
        for curse_dict in const.CURSE_LIST:
            response = re.sub(r"(?<![:\w*:])" + curse_dict["curse_word"], "*" + curse_dict["traduction"] + "*", response, flags=re.IGNORECASE)
        
        await message.delete()
        await message.channel.send(response)

    if "echec" in message.content.lower() or "échec" in message.content.lower():
        response = "https://tenor.com/bq4o5.gif"
        await message.channel.send(response)

    if "possible" in message.content.lower():
        response = "https://tenor.com/XiKZ.gif"
        await message.channel.send(response)


if __name__ == "__main__":
    bot.run(const.TOKEN) # See help here for the loggout message
