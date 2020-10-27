import re

import discord

import const


async def on_message_jokes(bot, message):

    if any(je_suis in message.content.lower() for je_suis in const.LIST_JE_SUIS):
        regex_je_suis = "(" + ")|(".join(const.LIST_JE_SUIS) + ")"
        i_am = re.split(regex_je_suis, message.content, 1, flags=re.IGNORECASE)[-1]
        response = f"Salut *{i_am}*, moi c'est le {bot.user.mention}"
        await message.channel.send(response)

    if "echec" in message.content.lower() or "échec" in message.content.lower():
        response = "https://tenor.com/bq4o5.gif"
        await message.channel.send(response)

    if "possible" in message.content.lower():
        response = "https://tenor.com/XiKZ.gif"
        await message.channel.send(response)
    
    if "aled" in message.content.lower():
        response ="https://assets.classicfm.com/2017/23/aled-jones-new-1497019550-editorial-long-form-1.png"
        await message.channel.send(response)
    
    if any(entry["word"].split(" ")[0].lower() in message.content.lower() for entry in const.DICO_MARSEILLAIS):
        present_words = [ entry for entry in const.DICO_MARSEILLAIS if entry["word"].split(" ")[0].lower() in message.content.lower() ]
        response = f"Hey <@{const.ANTOINE_TAG}>"
        for entry in present_words:
            word = entry["word"]
            description = entry["description"]
            response += f", \"{word}\" ça veut dire {description}"
        await message.channel.send(response)

    if any(re.search(r"(?<!\:)" + curse_dict["curse_word"], message.content, flags=re.IGNORECASE) for curse_dict in const.CURSE_LIST):
        response = message.content
        for curse_dict in const.CURSE_LIST:
            response = re.sub(r"(?<!\:)" + curse_dict["curse_word"], "*" + curse_dict["traduction"] + "*", response, 0, flags=re.IGNORECASE)

        response = f"{message.author.mention} : {response}"
        await message.delete()
        await message.channel.send(response)
