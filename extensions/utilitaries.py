# Utilitaries command for BotÀToutFer
import os
import random
import json
import re
import aiohttp
from bs4 import BeautifulSoup

import discord
from discord.ext import commands

import const


def setup(bot):
    bot.add_cog(Utilitaire(bot))


class Utilitaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="news", help="Donne le lien d'un ou plusieurs articles de presse du jour (par défaut 1)") # https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-web-request
    async def news(self, ctx, number_tiles: int=1):
        async with aiohttp.ClientSession() as session:
            self.bot.log.warning(f"Asking for the local news")
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

                    w_description = weather["weather"][0]["description"]
                    w_temp = round(weather["main"]["temp"], 1)
                    w_city = weather["name"]
                    w_country = weather["sys"]["country"]

                    self.bot.log.warning(f"Asking for the weather of the city {w_city} in {w_country} (id: {random_city})")
                    response = f"Actuellement {w_description}, il fait {w_temp} °C à {w_city} ({w_country}) :earth_africa:"
                    await ctx.send(response)


    @commands.command(name="scrabble", help="Donne les mots possibles au Scrabble avec une combinaison donnée (entrer une * pour saisir un joker)")
    async def scrabble(self, ctx, trestle=""):
        self.bot.log.warning(f"Scrabble command is invoked")

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

            if len(capitalized_word) >= 7: # If a word is 7 letters or more, we add a 50 points bonus
                value += 50

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
    async def inutile(self, ctx, number=1):
        number = min(number, 5)

        for _ in range(number):
            async with aiohttp.ClientSession() as session:
                self.bot.log.warning(f"Asking a useless piece of knowledge")
                async with session.get("https://www.savoir-inutile.com/") as r: # Retreve a useless piece of knowledge
                    if r.status == 200:
                        html = await r.text("utf-8")
                        soup = BeautifulSoup(html, "html.parser")

                        knowledge = soup.find(id="phrase").string
                        link = soup.find("meta", attrs={"name": "og:url"})["content"]
                        publication_date = soup.find("div", id="publication").find_all("span")[-1].string.strip()

                        embed = discord.Embed(
                            title="Savoir Inutile",
                            description=knowledge,
                            url=link
                        )
                        embed.add_field(
                            name="Date",
                            value=publication_date,
                            inline=True
                        )

                        await ctx.send(embed=embed)


    @commands.command(name="tv", help="Donne le programme de la TNT de ce soir")
    async def tv(self, ctx, channel_number=0):
        async with aiohttp.ClientSession() as session:
            self.bot.log.warning(f"Asking for the TNT programm of the night")
            async with session.get("https://www.programme-tv.net/programme/programme-tnt.html") as r: # Retreve the TNT programm of the night
                if r.status == 200:
                    html = await r.text("utf-8")

                    soup = BeautifulSoup(html, "html.parser")

                    date_and_hour = soup.find(class_="timeNavigationOverlay-currentDate").p.string
                    date_and_hour = " ".join(line.strip() for line in date_and_hour.split("\n") if line.strip())
                    date, hour = date_and_hour.split(" de ")

                    div_channels = soup.findAll(class_="doubleBroadcastCard") # List that contain div of all the channels
                    channels = {} # {1: "Sur la chaîne TF1 (Chaîne n°1) :...", 2: "Sur la chaîne France 2 (Chaîne n°2) :..."}

                    for channel in div_channels: # For all div in the list, we create a response with the programm of the channel
                        channel_name = channel.find(class_="doubleBroadcastCard-channel").a.string.strip()
                        channel_nb = channel.find(class_="doubleBroadcastCard-channelNumber").string.strip()

                        programm_hours = [ hour.string.strip() for hour in channel.findAll(class_="doubleBroadcastCard-hour") ]
                        programm_infos = channel.findAll(class_="doubleBroadcastCard-infos")
                        programm = []

                        channel_response= f"\n  Sur la chaîne {channel_name} ({channel_nb}) :\n"

                        for i in range(len(programm_hours)):
                            programm_title = programm_infos[i].find(class_="doubleBroadcastCard-title").string.strip()

                            if programm_infos[i].findAll(class_="doubleBroadcastCard-subtitle"):
                                programm_subtitle = programm_infos[i].findAll(class_="doubleBroadcastCard-subtitle")[0].string.strip()
                                programm_subtitle = " ".join(line.strip() for line in programm_subtitle.split("\n") if line.strip())
                                programm_title += " - " + programm_subtitle

                            programm_link = programm_infos[i].find(class_="doubleBroadcastCard-title")["href"]
                            programm_category = programm_infos[i].find(class_="doubleBroadcastCard-type").string.strip()
                            programm_hour = programm_hours[i]
                            programm_duration = programm_infos[i].find(class_="doubleBroadcastCard-durationContent").string.strip()

                            channel_response += f"    À {programm_hour} {programm_title}\n"

                        channel_nb = int(re.search(r"\d+", channel_nb)[0]) # The channel number (int) will be a key in the dictionnay
                        channels[channel_nb] = channel_response # Key: channel number (int). Value: channel programm (str)

                    if channel_number: # If the user ask for a specific channel
                        try: # We try to send the programm of the channel if any
                            response = f"```Programme de ce {date} soir :\n" + channels[channel_number] + "```"
                            await ctx.send(response)
                        except Exception:
                            await ctx.send("Je ne connais pas cette chaîne.")
                        finally:
                            return

                    else: # If the user DOESNT ask for a specific channel
                        response = f"```Programme de ce {date} soir :\n" # We create a new response string
                        for item in channels.values(): # For all the items in the dictionary
                            if len(response + item) + 3 < 2000: # If next channel can be added without exeed the Discord limit
                                response += item # We add the programm of the channel to the response
                            else: # If next channel CANNOT be added without exeed the Discord limit
                                response += "```"
                                await ctx.send(response) # We send the response
                                response = "```\n" # We create a new response
                                response += item # We add the programm of the channel to the new response
                        if len(response) > 3:# We exhaust all the dictionary, we send the last channels if any
                            response += "```"
                            await ctx.send(response)


    @commands.command(name="dico", help="Donne la définition du mot demandé")
    async def dico(self, ctx, word: str=""):
        if word:
            word = re.split("\W", word.lower())[0]
            async with aiohttp.ClientSession() as session:
                self.bot.log.warning(f"Asking for word definition")
                async with session.get(f"https://api.dicolink.com/v1/mot/{word}/definitions?limite=1&api_key={const.DICOLINK_TOKEN}") as r: # Retreve a definition
                    if r.status == 200:
                        definition = await r.json()
                        try:
                            response = f"Définition du mot \"{definition[0]['mot']}\" : {definition[0]['definition']}"
                        except KeyError as e:
                            response  = "Ce mot n'existe pas"
                        await ctx.send(response)


    @commands.command(name="marmiton", help="Retourne des recettes liées à un thème donné sur marmiton")
    async def marmiton(self, ctx, *, options:str=""):
        # marmiton_regex = r"^(\w+ ?)+(((-n|--nombre) \d+ ?)|((-p|--plat) (accompagnement ?|amusegueule ?|boisson ?|confiserie ?|conseil ?|dessert ?|entree ?|platprincipal ?|sauce ?)+)|((-d|--difficulte) (1 ?|2 ?|3 ?|4 ?)+)|((-c|--cout) (1 ?|2 ?|3 ?)+)|((-r|--restriction) (1 ?|2 ?|3 ?|4 ?)+)|((-t|--temps) (15 ?|30 ?|45 ?))|(--cuisson (1 ?|2 ?|3 ?)+)|((-s|-saison) ?))*$"
        try:
            options = options.strip()
            research = options.split(" -")[0]

            if research:

                try:
                    nb_recepies = int(re.search(r"((?<=-n )\d+|(?<=--nombre )\d+)", options)[0])
                except TypeError:
                    nb_recepies = 2

                try:
                    re_plats = r"((?<=-p )(accompagnement ?|amusegueule ?|boisson ?|confiserie ?|conseil ?|dessert ?|entree ?|platprincipal ?|sauce ?)+|(?<=--plat )(accompagnement ?|amusegueule ?|boisson ?|confiserie ?|conseil ?|dessert ?|entree ?|platprincipal ?|sauce ?)+)"
                    plats = re.search(re_plats, options)[0].split()
                except TypeError:
                    plats = []

                try:
                    re_difficulties = r"((?<=-d )(1 ?|2 ?|3 ?|4 ?)+|(?<=--difficulte )(1 ?|2 ?|3 ?|4 ?)+)"
                    difficulties = re.search(re_difficulties, options)[0].split()
                except TypeError:
                    difficulties = []

                try:
                    re_costs = r"((?<=-c )(1 ?|2 ?|3 ?)+|(?<=--cout )(1 ?|2 ?|3 ?)+)"
                    costs = re.search(re_costs, options)[0].split()
                except TypeError:
                    costs = []

                try:
                    re_restrictions = r"((?<=-r )(1 ?|2 ?|3 ?|4 ?)+|(?<=--restriction )(1 ?|2 ?|3 ?|4 ?)+)"
                    restrictions = re.search(re_restrictions, options)[0].split()
                except TypeError:
                    restrictions = []

                try:
                    re_time = r"((?<=-t )(15|30|45)|(?<=--temps )(15|30|45))"
                    max_time = re.search(re_time, options)[0].strip()
                except TypeError:
                    max_time = ""

                try:
                    re_cuissons = r"(?<=--cuisson )(1 ?|2 ?|3 ?)+"
                    cuissons = re.search(re_cuissons, options)[0].split()
                except TypeError:
                    cuissons = []

                saisonal = True if re.search(r"-s|--saison", options) else False

                http_params = []

                http_params.append(("aqt", research))

                for plat in plats:
                    http_params.append(("dt", plat))

                for difficulty in difficulties:
                    http_params.append(("dif", difficulty))

                for cost in costs:
                    http_params.append(("exp", cost))

                for restriction in restrictions:
                    http_params.append(("prt", restriction))

                if max_time:
                    http_params.append(("ttlt", max_time))
                
                for cuisson in cuissons:
                    http_params.append(("rct", cuisson))

                if saisonal:
                    http_params.append(("type", "season"))

                async with aiohttp.ClientSession() as session:
                    self.bot.log.warning(f"Asking recepies on marmiton")
                    async with session.get("https://www.marmiton.org/recettes/recherche.aspx", params=http_params) as r: # Retreve a marmiton page
                        if r.status == 200:
                            html = await r.text("utf-8")
                            soup = BeautifulSoup(html, "html.parser")

                            nb_results = soup.find(class_="recipe-search__nb-results").string.strip()
                            nb_results = int(re.search(r"\d+", nb_results)[0])

                            if nb_results:
                                div_results = soup.find("div", class_="recipe-results")
                                list_recipes = div_results.find_all(class_="recipe-card")
                                nb_recepies = min(nb_recepies, len(list_recipes))

                                response = f"{nb_results} résultat(s) trouvé sur Marmiton ! J'en affiche {nb_recepies}"
                                await ctx.send(response)

                                for i in range(nb_recepies):
                                    div_recipe = list_recipes[i]

                                    element_description = div_recipe.find(class_="recipe-card__description").contents
                                    description = ""
                                    for element in element_description:
                                        if element == "\n":
                                            continue
                                        try:
                                            description += str(element.contents[0])
                                        except Exception:
                                            description += str(element)
                                    description = description.replace("<br/>", "\n")

                                    div_rating = div_recipe.find(class_="recipe-card__rating")
                                    rating = div_rating.find(class_="recipe-card__rating__value").string.strip()
                                    rating += " " + div_rating.find(class_="recipe-card__rating__value__fract").string.strip()
                                    rating += " " + div_rating.find(class_="mrtn-font-discret").string.strip()

                                    embed = discord.Embed(
                                        title=div_recipe.find("h4").string.strip(),
                                        description=description,
                                        url="https://www.marmiton.org" + div_recipe.find("a", class_="recipe-card-link")["href"],
                                        color=0xFF9B90
                                    )
                                    embed.set_thumbnail(
                                        url=div_recipe.find("img")["data-src"]
                                    )
                                    embed.set_author(
                                        name=ctx.author.name,
                                        icon_url=ctx.author.avatar_url
                                    )
                                    embed.add_field(
                                        name="Durée",
                                        value=div_recipe.find(class_="recipe-card__duration__value").string.strip(),
                                        inline=True
                                    )
                                    embed.add_field(
                                        name="Note",
                                        value=rating,
                                        inline=True
                                    )

                                    if div_recipe.find(class_="recipe-card__sponsored"):
                                        sponsor = re.search(r"(?<=\[).+(?=\])", div_recipe.find(class_="recipe-card-link")["onclick"], re.IGNORECASE)[0]
                                        embed.add_field(
                                            name="Contenu sponsorisé",
                                            value=sponsor,
                                            inline=True
                                        )

                                    await ctx.send(embed=embed)

                            else:
                                response = "Désolé, je n'ai pas trouvé de résultats..."
                                return await ctx.send(response)

            else: # Display help
                response = ("```\n" +
                            "Usage :\n" +
                            "  !marmiton <nom de la recherche> [--options <arguments>...]\n" +
                            "\n" +
                            "Options :\n" +
                            "  -n <argument>, --nombre <argument>             Précise le nombre de recettes à retourner [défaut : 2]\n" +
                            "  -p <argument>..., --plat <argument>...         Précise un ou plusieurs types de plats parmi : accompagnement, amusegueule, boisson, confiserie, conseil, dessert, entree, platprincipal, sauce\n" +
                            "  -d <argument>..., --difficulte <argument>...   Précise un ou plusieurs niveau de difficulté parmi : 1 (très facile), 2 (facile), 3 (moyen), 4 (difficile)\n" +
                            "  -c <argument>..., --cout <argument>...         Précise un ou plusieurs coût de recette parmi : 1 (bon marché), 2 (coût moyen), 3 (assez cher)\n" +
                            "  -r <argument>..., --restriction <argument>...  Précise une ou plusieurs restriction alimentaire parmi : 1 (végétarien), 2 (sans gluten), 3 (végan), 4 (sans lactose)\n" +
                            "  -t <argument>, --temps <argument>              Précise le temps maximum de la recette parmi : 15, 30, 45\n" +
                            "  --cuisson <argument>...                        Précise un ou plusieurs type de cuisson parmi : 1 (four), 2 (micro-ondes), 3 (aucun)\n" +
                            "  -s, --saison                                   Précise si la recette doit être de saison\n" +
                            "```\n")
                await ctx.send(response)

        except Exception as e:
            self.bot.log.exception(f"Unable to send a marmiton recipe in this channel: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})")
            await ctx.send("Something went wrong https://tenor.com/s8CP.gif")
