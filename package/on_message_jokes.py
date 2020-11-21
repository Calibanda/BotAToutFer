import re

import discord

import const


async def joke_je_suis(bot, message):
    if any(je_suis in message.content.lower() for je_suis in const.LIST_JE_SUIS):
        regex_je_suis = "(" + ")|(".join(const.LIST_JE_SUIS) + ")" # "(je suis)|(j'suis)|(chuis) ..."
        i_am = re.split(regex_je_suis, message.content, 1, flags=re.IGNORECASE)[-1]
        response = f"Salut *{i_am}*, moi c'est le {bot.user.mention}"
        await message.channel.send(response)


async def joke_echec(message, words_in_message):
    if [ word for word in words_in_message if word in {"échec", "echec"} ]: # If common words between words in the original message and "échec" or "echec"
        response = "https://tenor.com/bq4o5.gif"
        await message.channel.send(response)


async def joke_possible(message, words_in_message):
    if [ word for word in words_in_message if word in {"possible", "impossible"} ]: # If common words between words in the original message and "possible" or "impossible"
        response = "https://tenor.com/XiKZ.gif"
        await message.channel.send(response)


async def joke_aled(message, words_in_message):
    if "aled" in words_in_message: # If the word "aled" in the original message
        response ="https://assets.classicfm.com/2017/23/aled-jones-new-1497019550-editorial-long-form-1.png"
        await message.channel.send(response)


async def mousse(message, words_in_message):
    if "attention" in words_in_message or "mousse" in words_in_message: # If the words "attention" or "mousse" in the original message
        response ="https://media1.tenor.com/images/ef6a3c5ba7cbdc4b0140d7363dbc841f/tenor.gif" # Send the "ATTENTION À LA MOUSSE !!" gif
        await message.channel.send(response)


async def projet(message, words_in_message):
    if "projet" in words_in_message: # If the words "projet" in the original message
        response ="https://tenor.com/RGiO.gif" # Send the "CAR C'EST NOTRE PROJEEEEET !!" gif
        await message.channel.send(response)


async def cursed_words(message, words_in_message):
    if [ word for word in words_in_message for curse_dict in const.CURSE_LIST if word == curse_dict["curse_word"] ]: # If any curse word in the original message
        response = message.content
        for curse_dict in const.CURSE_LIST:
            response = re.sub(r"(?<!\:)" + curse_dict["curse_word"], "*" + curse_dict["traduction"] + "*", response, 0, flags=re.IGNORECASE)

        response = f"{message.author.mention} : {response}"
        await message.channel.send(response)
        await message.delete()


async def marseillais_word(message, words_in_message):
    present_words = [ entry for entry in const.DICO_MARSEILLAIS for word in words_in_message if word == entry["word"].split(" ")[0].lower() ] # Catch all the marseillais words
    if present_words: # If any marseillais word in the original message
        response = f"Hey <@{const.ANTOINE_TAG}>, "
        for entry in present_words:
            word = entry["word"]
            description = entry["description"]
            response += f"\"{word}\" ça veut dire {description}\n"
        response = response[:-1]
        await message.channel.send(response)


async def on_message_jokes(bot, message):

    words_in_message = [ word for word in re.split("\W", message.content.lower()) if word ] # We split the words in the message on any non word character (\W) and ignore empty words

    await joke_je_suis(bot, message)
    await joke_echec(message, words_in_message)
    await joke_possible(message, words_in_message)
    await joke_aled(message, words_in_message)
    await cursed_words(message, words_in_message)
    await mousse(message, words_in_message)
    await projet(message, words_in_message)
    # await marseillais_word(message, words_in_message)
