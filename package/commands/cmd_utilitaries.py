# Utilitaries command for BotAToutFer
import os
import random
import json
import aiohttp
from bs4 import BeautifulSoup

from discord.ext import commands

import const

class Utilitaire(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger
        self._last_member = None

    @commands.command(name="news", help="Donne le lien d'un ou plusieurs articles de presse du jour (par défaut 1)") # https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-web-request
    async def news(self, ctx, number_tiles: int=1):
        async with aiohttp.ClientSession() as session:
            self.logger.warning(f"Asking for the local news")
            async with session.get(f"http://newsapi.org/v2/top-headlines?country=fr&apiKey={const.NEWS_TOKEN}") as r: # Retreve last news
                if r.status == 200:
                    news = await r.json()

                    old_news = []

                    if os.path.isfile(const.LAST_NEWS_URL_PATH):
                        with open(const.LAST_NEWS_URL_PATH, "r") as f:
                            try:
                                old_news = json.load(f) # We try to load the news who have already been displayed by the bot
                            except Exception:
                                pass

                    today_news = [ article["url"] for article in news["articles"] if article["url"] not in old_news ] # We retreve all the url that hasn't been already displayed
                    news_to_display = today_news[:number_tiles] # We keep at most the number of articles asked from the user

                    if not news_to_display:
                        await ctx.send("Pas de nouveaux articles en ce moment, réessaye plus tard.")
                        return

                    for news in news_to_display:
                        await ctx.send(news)

                    old_news = old_news + news_to_display # We add the just displayed news to the old ones

                    with open(const.LAST_NEWS_URL_PATH, "w") as f:
                        json.dump(old_news[-25:], f, indent=4) # We store the 25 most recent displayed articles in a json file


    @commands.command(name="meteo", help="Donne la météo (d'une ville au hasard dans le monde)") # https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-web-request
    async def meteo(self, ctx):
        with open(os.path.join(const.SCRIPT_DIR, "package", "list_city_id.json"), "r") as f:
            list_city_id = json.load(f)

        random_city = random.choice(list_city_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.openweathermap.org/data/2.5/weather?id={random_city}&appid={const.WEATHER_TOKEN}&units=metric&lang=fr") as r:

                if r.status == 200:
                    weather = await r.json()

                    #weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={random_city}&appid={WEATHER_TOKEN}&units=metric&lang=fr").json()
                    self.logger.warning("Asking for the weather of the city " + weather["name"] + " in " + weather["sys"]["country"] + f" (id: {random_city})")
                    w_description = weather["weather"][0]["description"]
                    w_temp = round(weather["main"]["temp"], 1)
                    response = f"Actuellement {w_description}, il fait {w_temp} °C (quelque part dans le monde :earth_africa:)."
                    await ctx.send(response)


    @commands.command(name="scrabble", help="Donne les mots possibles au Scrabble avec une combinaison donnée (entrer une * pour saisir un joker)")
    async def scrabble(self, ctx, trestle=""):
        self.logger.warning(f"Scrabble command is invoked")

        if not trestle.strip():
            response = "Utilise la commande '!scrabble' suivie de ton chevalet pour que je puisse te donner les combnaisons possible (entre une * pour saisir un joker)."
            await ctx.send(response)
            return

        def convert_word(word):
            word = word.upper()
            word = word.replace('\n', '')
            word = word.replace('-', '')
            word = word.replace('À', 'A')
            word = word.replace('Â', 'A')
            word = word.replace('Ä', 'A')
            word = word.replace('Ç', 'C')
            word = word.replace('É', 'E')
            word = word.replace('È', 'E')
            word = word.replace('Ê', 'E')
            word = word.replace('Ë', 'E')
            word = word.replace('Î', 'I')
            word = word.replace('Ï', 'I')
            word = word.replace('Ô', 'O')
            word = word.replace('Ö', 'O')
            word = word.replace('Ù', 'U')
            word = word.replace('Û', 'U')
            word = word.replace('Ü', 'U')
            word = word.replace('Ÿ', 'Y')
            word = word.replace('Œ', 'OE')

            return word


        def compare_word(trestle, word):
            total_difference = 0
            list_letters_to_ignore = []
            for letter in word:
                if letter not in list_letters_to_ignore:
                    difference = word.count(letter) - trestle.count(letter)
                    list_letters_to_ignore.append(letter)
                    if difference > 0:
                        total_difference += difference

            return total_difference


        def add_dico(dico_possible_words, trestle, word):
            value = 0
            capitalized_word = ""

            for lettre in word:
                if lettre in trestle:
                    value += const.FRENCH_SCRABBLE_VALUES[lettre]
                    capitalized_word = capitalized_word + lettre
                    trestle = trestle.replace(lettre, '', 1)
                else:
                    capitalized_word = capitalized_word + lettre.lower()

            dico_possible_words[capitalized_word] = value

            return dico_possible_words


        def create_response(dico_possible_words):
            response = "Voici la liste des mots disponibles avec les lettres de votre chevalet :\n```\n"
            while len(dico_possible_words) > 0:
                maximum_value = max(dico_possible_words.copy().values())
                for key, value in dico_possible_words.copy().items():
                    if value == maximum_value:
                        response += f"{value} point(s) : {key}\n"
                        del dico_possible_words[key]
            
            response += "```"
            return response


        with open(const.SCRABBLE_DICTIONARY_PATH, "r", encoding="utf-8") as scrabble_disctionary:

            dico_possible_words = {}
            trestle = convert_word(trestle)

            lines = scrabble_disctionary.readlines()

            for line in lines:
                word = convert_word(line)
                if compare_word(trestle, word) <= trestle.count('*'):
                    dico_possible_words = add_dico(dico_possible_words, trestle, word)

            response = create_response(dico_possible_words)
            await ctx.send(response)


    @commands.command(name="inutile", help="Donne un savoir inutile")
    async def scrabble(self, ctx, number=1):
        number = min(number, 5)

        for _ in range(number):
            async with aiohttp.ClientSession() as session:
                self.logger.warning(f"Asking a useless piece of knowledge")
                async with session.get("https://www.savoir-inutile.com/") as r: # Retreve a useless piece of knowledge
                    if r.status == 200:
                        html = await r.text("utf-8")
                        soup = BeautifulSoup(html, "html.parser")

                        knowledge = soup.find(id="phrase").string
                        link = soup.find("meta", attrs={"name": "og:url"})["content"]
                        publication_date = soup.find("div", id="publication").find_all("span")[-1].string.strip()

                        response = f"{knowledge}\nSavoir inutile posté le {publication_date}. {link}"
                        await ctx.send(response)
