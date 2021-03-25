# Utilities command for BotÀToutFer
import os
import random
import json
import re
from bs4 import BeautifulSoup

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Utilitaire(bot))


class Utilitaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.LAST_NEWS_URL_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "last_news_url.json"
        )  # Path of the json file containing the latest retrieved news
        self.NEWS_API_URL = "http://newsapi.org/v2/top-headlines"
        self.NEWS_API_PARAMS = {"country": "fr", "apiKey": self.bot.NEWS_TOKEN}

        self.CITY_ID_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "list_city_id.json"
        )
        self.WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
        self.WEATHER_API_PARAMS = {"id": "", "appid": self.bot.WEATHER_TOKEN, "units": "metric", "lang": "fr"}

        self.SCRABBLE_DICTIONARY_PATH = os.path.join(
            self.bot.SCRIPT_DIR,
            "package",
            "ODS7.txt"
        )  # Path of the french scrabble dictionary
        self.FRENCH_SCRABBLE_VALUES = {
            "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4,
            "I": 1, "J": 8, "K": 10, "L": 1, "M": 2, "N": 1, "O": 1, "P": 3,
            "Q": 8, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 10, "X": 10,
            "Y": 10, "Z": 10
        }

        self.KNOWLEDGE_URL = "https://www.savoir-inutile.com/"

        self.TV_URL = "https://www.programme-tv.net/programme/programme-tnt.html"

        self.MARMITON_URL = "https://www.marmiton.org/recettes/recherche.aspx"

    @commands.command(name="news", help="Donne le lien d'un ou plusieurs articles de presse du jour (par défaut 1)")
    async def news(self, ctx, number_tiles: int=1):
        self.bot.log.warning(f"Asking for the local news")
        async with self.bot.http_session.get(url=self.NEWS_API_URL, params=self.NEWS_API_PARAMS) as r:  # Retrieve last news
            if r.status == 200:
                news = await r.json()

                try:
                    # We try to load the news that have already
                    # been displayed by the bot
                    with open(self.LAST_NEWS_URL_PATH, "r") as f:
                        old_news = json.load(f)
                except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
                    self.bot.log.error("last_news_url.json file not found: ", exc_info=e)
                    old_news = []

                # We retrieve all the url that hasn't
                # been already displayed
                today_news = []
                for article in news["articles"]:
                    if article["url"] not in old_news:
                        today_news.append(article["url"])

                # We keep at most the number of articles asked
                # from the user
                news_to_display = today_news[:number_tiles]

                if not news_to_display:
                    response = "Pas de nouveaux articles en ce moment, réessaye plus tard."
                    await ctx.send(response)
                    return

                for news in news_to_display:
                    await ctx.send(news)

                # We add the just displayed news to the old ones
                old_news = old_news + news_to_display

                with open(self.LAST_NEWS_URL_PATH, "w") as f:
                    # We store the 25 most recent displayed articles
                    # in a json file
                    json.dump(old_news[-25:], f, indent=4)

    @commands.command(name="meteo", help="Donne la météo (d'une ville au hasard dans le monde)")
    async def meteo(self, ctx):
        try:
            with open(self.CITY_ID_PATH, "r") as f:
                list_city_id = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.bot.log.error("No list_city_id.json file: ", exc_info=e)
            await ctx.send("Unable to load the city list")
            return

        random_city_id = random.choice(list_city_id)

        async with self.bot.http_session.get(url=self.WEATHER_API_URL, params=self.WEATHER_API_PARAMS | {"id": str(random_city_id)}) as r:
            if r.status == 200:
                weather = await r.json()

                w_description = weather["weather"][0]["description"]
                w_temp = round(weather["main"]["temp"], ndigits=1)
                w_city = weather["name"]
                w_country = weather["sys"]["country"]

                self.bot.log.warning(f"Asking for the weather of the city {w_city} in {w_country} (id: {random_city_id})")
                response = f"Actuellement {w_description}, il fait {w_temp} °C à {w_city} ({w_country}) :earth_africa:"
                await ctx.send(response)

    @commands.command(name="scrabble", help="Donne les mots possibles au Scrabble avec une combinaison donnée (entrer une * pour saisir un joker)")
    async def scrabble(self, ctx, trestle=""):
        self.bot.log.warning(f"Scrabble command is invoked")

        if not trestle.strip():
            response = (
                "Utilise la commande '!scrabble' suivie de ton chevalet "
                + "pour que je puisse te donner les combinaisons possible "
                + "(entre une * pour saisir un joker)."
            )
            await ctx.send(response)
            return

        def convert_word(word):
            return word.upper()\
                .replace('\n', '')\
                .replace('-', '')\
                .replace('À', 'A')\
                .replace('Â', 'A')\
                .replace('Ä', 'A')\
                .replace('Ç', 'C')\
                .replace('É', 'E')\
                .replace('È', 'E')\
                .replace('Ê', 'E')\
                .replace('Ë', 'E')\
                .replace('Î', 'I')\
                .replace('Ï', 'I')\
                .replace('Ô', 'O')\
                .replace('Ö', 'O')\
                .replace('Ù', 'U')\
                .replace('Û', 'U')\
                .replace('Ü', 'U')\
                .replace('Ÿ', 'Y')\
                .replace('Œ', 'OE')

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
                    value += self.FRENCH_SCRABBLE_VALUES[lettre]
                    capitalized_word = capitalized_word + lettre
                    trestle = trestle.replace(lettre, '', 1)
                else:
                    capitalized_word = capitalized_word + lettre.lower()

            if len(capitalized_word) >= 7:
                # If a word is 7 letters or more, we add a 50 points bonus
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

        dico_possible_words = {}
        trestle = discord.utils.escape_markdown(trestle)
        trestle = convert_word(trestle)

        try:
            with open(self.SCRABBLE_DICTIONARY_PATH, "r", encoding="utf-8") as scrabble_dictionary:
                lines = scrabble_dictionary.readlines()
        except FileNotFoundError as e:
            self.bot.log.error("No ODS7.txt file: ", exc_info=e)
            response = "Il n'y a pas de dictionnaire pour chercher le mot !"
            await ctx.send(response)
        else:
            for line in lines:
                word = convert_word(line)
                if compare_word(trestle, word) <= trestle.count('*'):
                    dico_possible_words = add_dico(
                        dico_possible_words, trestle, word
                    )

            response = create_response(dico_possible_words)
            await ctx.send(response)

    @commands.command(name="inutile", help="Donne un savoir inutile")
    async def inutile(self, ctx, number=1):
        for _ in range(min(number, 5)):
            self.bot.log.warning(f"Asking a useless piece of knowledge")
            async with self.bot.http_session.get(url=self.KNOWLEDGE_URL) as r:
                # Retrieve a useless piece of knowledge
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
        self.bot.log.warning(f"Asking for the TNT program of the night")
        async with self.bot.http_session.get(url=self.TV_URL) as r:
            # Retrieve the TNT program of the night
            if r.status == 200:
                html = await r.text("utf-8")

                soup = BeautifulSoup(html, "html.parser")

                date_and_hour = soup.find(class_="timeNavigationOverlay-currentDate").p.string

                list_date_and_hour = []
                for line in date_and_hour.split("\n"):
                    if line.strip():
                        list_date_and_hour.append(line.strip())

                date_and_hour = " ".join(list_date_and_hour)

                date, hour = date_and_hour.split(" de ")

                # List that contain div of all the channels
                div_channels = soup.findAll(class_="bouquet-cards")
                channels = {}
                # {1: "Sur la chaîne TF1 (Chaîne n°1) :...",
                # 2: "Sur la chaîne France 2 (Chaîne n°2) :..."}

                for channel in div_channels:
                    # For all div in the list, we create a response
                    # with the program of the channel
                    channel_name = channel.find(class_="bouquet-cardsChannelItemLink")["title"].strip()
                    channel_nb = channel.find(class_="bouquet-channelNumber").string.strip()

                    channel_response = f"\n  Sur la chaîne {channel_name} ({channel_nb}) :\n"

                    programs_div = channel.findAll(class_=["first", "last"])
                    for program_div in programs_div:
                        program_title = program_div.find(class_="mainBroadcastCard-title").a.string.strip()
                        try:
                            program_subtitle = program_div.find(class_="mainBroadcastCard-subtitle").string.strip()
                        except AttributeError as e:
                            pass
                        else:
                            program_title += " - " + program_subtitle

                        program_hour = program_div.find(class_="mainBroadcastCard-startingHour").string.strip()

                        channel_response += f"    À {program_hour} {program_title}\n"

                    # The channel number (int) will be a key
                    # in the dictionary
                    channel_nb = int(re.search(r"\d+", channel_nb)[0])

                    # Key: channel number (int).
                    # Value: channel program (str)
                    channels[channel_nb] = channel_response

                if channel_number:
                    # If the user ask for a specific channel
                    try:
                        # We try to send the program of the channel if any
                        response = (
                            f"```Programme de ce {date} soir :\n"
                            + channels[channel_number]
                            + "```"
                        )
                        await ctx.send(response)
                    except KeyError as e:
                        await ctx.send("Je ne connais pas cette chaîne.")
                    finally:
                        return

                else:  # If the user DOESNT ask for a specific channel
                    # We create a new response string
                    response = f"```Programme de ce {date} soir :\n"
                    for item in channels.values():
                        # For all the items in the dictionary
                        if len(response + item) + 3 < 2000:
                            # If next channel can be added
                            # without exceed the Discord limit,
                            # we add the program of the channel
                            # to the response
                            response += item
                        else:
                            # If next channel CANNOT be added
                            # without exceed the Discord limit
                            response += "```"
                            await ctx.send(response)
                            response = "```\n"  # We create a new response
                            # We add the program of
                            # the channel to the new response
                            response += item
                    if len(response) > 3:
                        # We exhaust all the dictionary,
                        # we send the last channels if any
                        response += "```"
                        await ctx.send(response)

    @commands.command(name="dico", help="Donne la définition du mot demandé")
    async def dico(self, ctx, word: str=""):
        if word:
            word = re.split("\W", word.lower())[0]
            self.bot.log.warning(f"Asking for word definition")
            url = f"https://api.dicolink.com/v1/mot/{word}/definitions"
            params = {"limite": "1", "api_key": self.bot.DICOLINK_TOKEN}
            async with self.bot.http_session.get(url=url, params=params) as r:  # Retrieve a definition
                if r.status == 200:
                    definition = await r.json()
                    try:
                        response = (
                            f"Définition du mot "
                            + f"\"{definition[0]['mot']}\" : "
                            + f"{definition[0]['definition']}"
                        )
                    except KeyError as e:
                        response = "Ce mot n'existe pas"
                    await ctx.send(response)

    @commands.command(name="marmiton", help="Retourne des recettes liées à un thème donné sur marmiton")
    async def marmiton(self, ctx, *, options:str=""):
        # marmiton_regex = r"^(\w+ ?)+(((-n|--nombre) \d+ ?)|((-p|--plat)
        # (accompagnement ?|amusegueule ?|boisson ?|confiserie ?|conseil
        # ?|dessert ?|entree ?|platprincipal ?|sauce ?)+)|((-d|--difficulte)
        # (1 ?|2 ?|3 ?|4 ?)+)|((-c|--cout) (1 ?|2 ?|3 ?)+)|((-r|--restriction)
        # (1 ?|2 ?|3 ?|4 ?)+)|((-t|--temps) (15 ?|30 ?|45 ?))|(--cuisson
        # (1 ?|2 ?|3 ?)+)|((-s|-saison) ?))*$"
        try:
            options = options.strip()
            research = options.split(" -")[0]

            if research:

                try:
                    nb_recipes = int(re.search(
                        r"((?<=-n )\d+|(?<=--nombre )\d+)", options
                    )[0])
                except TypeError:
                    nb_recipes = 2

                try:
                    re_plats = (
                        r"((?<=-p )(accompagnement ?|amusegueule ?|boisson "
                        + r"?|confiserie ?|conseil ?|dessert ?|entree "
                        + r"?|platprincipal ?|sauce ?)+|(?<=--plat )"
                        + r"(accompagnement ?|amusegueule ?|boisson "
                        + r"?|confiserie ?|conseil ?|dessert ?|entree "
                        + r"?|platprincipal ?|sauce ?)+)"
                    )
                    plats = re.search(re_plats, options)[0].split()
                except TypeError:
                    plats = []

                try:
                    re_difficulties = (
                        r"((?<=-d )(1 ?|2 ?|3 ?|4 ?)+|(?<=--difficulte )"
                        + r"(1 ?|2 ?|3 ?|4 ?)+)"
                    )
                    difficulties = re.search(
                        re_difficulties,
                        options
                    )[0].split()
                except TypeError:
                    difficulties = []

                try:
                    re_costs = (
                        r"((?<=-c )(1 ?|2 ?|3 ?)+|(?<=--cout )"
                        + r"(1 ?|2 ?|3 ?)+)"
                    )
                    costs = re.search(re_costs, options)[0].split()
                except TypeError:
                    costs = []

                try:
                    re_restrictions = (
                        r"((?<=-r )(1 ?|2 ?|3 ?|4 ?)+|(?<=--restriction )"
                        + "(1 ?|2 ?|3 ?|4 ?)+)"
                    )
                    restrictions = re.search(
                        re_restrictions,
                        options
                    )[0].split()
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

                if re.search(r"-s|--saison", options):
                    seasonal = True
                else:
                    seasonal = False

                http_params = [("aqt", research)]

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

                if seasonal:
                    http_params.append(("type", "season"))

                self.bot.log.warning(f"Asking recipes on marmiton")
                async with self.bot.http_session.get(url=self.MARMITON_URL, params=http_params) as r:
                    # Retrieve a marmiton page
                    if r.status == 200:
                        html = await r.text("utf-8")
                        soup = BeautifulSoup(html, "html.parser")

                        nb_results = soup.find("span", class_="SearchSummarystyle__ResultNumber-sc-16jp16z-2").text.strip()
                        nb_results = int(re.search(r"\d+", nb_results)[0])

                        if nb_results:
                            div_results = soup.find("div", class_="SearchResultsstyle__Layout-sc-1gofnyi-0")
                            list_recipes = div_results.find_all(class_="SearchResultsstyle__SearchCardResult-sc-1gofnyi-2")
                            nb_recipes = min(nb_recipes, len(list_recipes))

                            response = f"{nb_results} résultat(s) trouvé sur Marmiton ! J'en affiche {nb_recipes}"
                            await ctx.send(response)

                            for i in range(nb_recipes):
                                div_recipe = list_recipes[i]

                                recipe_title = div_recipe.find("h4").text.strip()

                                rating = div_recipe.find(class_="MuiTypography-root MuiTypography-caption").text.strip()
                                rating += " " + div_recipe.find(class_="RecipeCardResultstyle__RatingNumber-sc-30rwkm-3 jtNPhW").text.strip()

                                recipe_url = "https://www.marmiton.org" + div_recipe["href"]

                                recipe_thumbnail = div_recipe.find("img")["src"]

                                recipe_is_sponsor = True if div_recipe.find(class_="RecipeCardResultstyle__SponsoredLabel-sc-30rwkm-1 jitMUn") else False

                                embed = discord.Embed(
                                    title=recipe_title,
                                    url=recipe_url,
                                    color=0xFF9B90
                                )
                                embed.set_thumbnail(
                                    url=recipe_thumbnail
                                )
                                embed.set_author(
                                    name=ctx.author.name,
                                    icon_url=ctx.author.avatar_url
                                )
                                embed.add_field(
                                    name="Note",
                                    value=rating,
                                    inline=True
                                )

                                if recipe_is_sponsor:
                                    embed.add_field(
                                        name="Contenu sponsorisé",
                                        value=":money_mouth:",
                                        inline=True
                                    )

                                await ctx.send(embed=embed)

                        else:
                            response = "Désolé, je n'ai pas trouvé de résultats..."
                            return await ctx.send(response)

            else:  # Display help
                response = (
                    "```\n"
                    + "Usage :\n"
                    + "  !marmiton <nom de la recherche> [--options <arguments>...]\n"
                    + "\n"
                    + "Options :\n"
                    + "  -n <argument>, --nombre <argument>             Précise le nombre de recettes à retourner [défaut : 2]\n"
                    + "  -p <argument>..., --plat <argument>...         Précise un ou plusieurs types de plats parmi : accompagnement, amusegueule, boisson, confiserie, conseil, dessert, entree, platprincipal, sauce\n"
                    + "  -d <argument>..., --difficulte <argument>...   Précise un ou plusieurs niveau de difficulté parmi : 1 (très facile), 2 (facile), 3 (moyen), 4 (difficile)\n"
                    + "  -c <argument>..., --cout <argument>...         Précise un ou plusieurs coût de recette parmi : 1 (bon marché), 2 (coût moyen), 3 (assez cher)\n"
                    + "  -r <argument>..., --restriction <argument>...  Précise une ou plusieurs restriction alimentaire parmi : 1 (végétarien), 2 (sans gluten), 3 (végan), 4 (sans lactose)\n"
                    + "  -t <argument>, --temps <argument>              Précise le temps maximum de la recette parmi : 15, 30, 45\n"
                    + "  --cuisson <argument>...                        Précise un ou plusieurs type de cuisson parmi : 1 (four), 2 (micro-ondes), 3 (aucun)\n"
                    + "  -s, --saison                                   Précise si la recette doit être de saison\n"
                    + "```\n"
                )
                await ctx.send(response)

        except Exception as e:
            self.bot.log.exception(f"Unable to send a marmiton recipe in this channel: {ctx.channel.guild}, #{ctx.channel.name} ({ctx.channel.id})", exc_info=e)
            await ctx.send("Something went wrong https://tenor.com/s8CP.gif")
