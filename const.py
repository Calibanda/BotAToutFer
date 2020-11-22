# const.py
import os
import datetime
import json

from dotenv import load_dotenv

SCRIPT_DIR, SCRIPT_FILENAME = os.path.split(os.path.abspath(__file__))

load_dotenv() # Loads tokens form env
TOKEN = os.getenv("DISCORD_TOKEN")
#GUILD = os.getenv("DISCORD_GUILD")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
NEWS_TOKEN = os.getenv("NEWS_TOKEN")
CAT_TOKEN = os.getenv("CAT_TOKEN")
#ANTOINE_TAG = int(os.getenv("ANTOINE_TAG"))
COFFEE_URL = os.getenv("COFFEE_URL")
COFFEE_TOKEN = os.getenv("COFFEE_TOKEN")

AUTORIZED_CHANNELS = [
    763426416167485481, # La crème de la crème > bot-test
    777901703697661982, # La crème de la crème > santa-secret
    777200257992884230, # Test bot > général
    777839870252285982, # CEH > bot
    ]

LOG_DIR = os.path.join(SCRIPT_DIR, "logs") # The directory containing logs
LOG_FILE_PATH = os.path.join(LOG_DIR, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log") # Absolute path of the new log file

LAST_NEWS_URL_PATH = os.path.join(SCRIPT_DIR, "package", "last_news_url.json")

BOT_DESCRIPTION = "BotAToutFer, le bot qui fait tout, même le café !"

CURSE_LIST = [
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

SCRABBLE_DICTIONARY_PATH = os.path.join(SCRIPT_DIR, "package", "ODS7.txt")

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

brooklyn_99_quotes = [
    "I'm the human form of the :100: emoji.",
    "Bingpot!",
    "Cool. Cool cool cool cool cool cool cool, no doubt no doubt no doubt no doubt.",
    "Every time someone steps up and says who they are, the world becomes a better, more interesting place.",
    "Haha, the angel puked!",
    "- I'm not a thug, I'm police.\n- Ok, then name one law.\n- Don't kill people?\n- It's on me. I set the bar too low...",
    "https://tenor.com/VdlE.gif",
    "YOU PUNK!",
    "Clearly, the pineapple IS the slut.",
    "It's time to sauce up!",
    "Oh, damn",
    "Eyes up here, Gina. I'm more than just a piece of ass.",
    "The only thing I’m not good at is modesty, because I’m great at it.",
    "The English language cannot fully capture the depth and complexity of my thoughts, so I’m incorporating emoji into my speech to better express myself. Winky face.",
    "Your butt is the bomb.",
    "\"Grave\" singular? Charles, \"grave\" singular?",

]

the_good_place_quotes = [
    "Everything is fine",
    "I'm telling you, Molotov cocktails work. Anytime I had a problem and I threw a Molotov cocktail, boom! Right away, I had a different problem.",
    "Not a girl",
    "Come on, you know how this works. You fail and then you try something else. And you fail again and again, and you fail a thousand times, and you keep trying because maybe the 1,001st idea might work. Now, I'm gonna and try to find our 1,001st idea.",
    "We do nothing. We hope that our early successes make up for the embarrassing mess we've become. Like Facebook. Or America.",
    "It turns out life isn't a puzzle that can be solved one time and it's done. You wake up every day, and you solve it again.",
    "You said that every human is a little bit sad all the time, because you know you're going to die. But that knowledge is what gives life meaning.",
    "This is what we've been looking for since the day we met. Time. That's what the Good Place really is — it's not even a place, really. It's just having enough time with the people you love.",
    "Okay homies, you're sad. I can tell 'cause you have the same looks on your faces that my teachers did whenever I raised my hand in class. But let's be happy.",
    "Picture a wave in the ocean. You can see it, measure it, its height, the way the sunlight refracts when it passes through, and it's there, and you can see it, you know what it is. It's a wave. And then it crashes on the shore, and it's gone. But the water is still there. The wave was just a different way for the water to be for a little while.",
    "You know what I just discovered recently? Podcasts. There's, like, a billion of them and they just keep coming.",
    "Here's an idea. What if we don't worry about whatever comes next?",
    "If there were an answer I could give you to how the universe works, it wouldn’t be special. It would just be machinery fulfilling its cosmic design. It would just be a big, dumb food processor. But since nothing seems to make sense, when you find something or someone that does, it's euphoria.",
    "In case you were wondering, I am, by definition, the best version of myself.",
    "Principles aren't principles when you pick and choose when you're gonna follow them.",
    "It's a rare occurrence, like a double rainbow. Or like someone on the internet saying, \"You know what? You’ve convinced me I was wrong.\"",
    "Now we're going to do the most human thing of all: attempt something futile with a ton of unearned confidence and fail spectacularly!",
    "Okay, shouldn't take long. Between an hour and, um, 11 months.",
    "Attention... I have been murdered.",
    "Now, all of you, get the fork out of my neighborhood.",
    "Holy motherforking shirtballs",
    "Ya basic",
    "I wasn't a failed DJ, I was pre-successful.",
    "Well fork you too",
    "Do you have a second to eat my farts?",
    "Hashtag Tahani time.",

]

sherlock_quotes = [
    "I'm not an addict, I'm a user. I alleviate boredom and occasionally heighten my thought processes.",
    "Nothing made me. I made me.",
    "Bravery is by far the kindest word for stupidity.",
    "Fear is wisdom in the face of danger, it is nothing to be ashamed of.",
    "Stress can ruin everyday of your life, dying can only ruin one.",
    "Good afternoon. I am Sherlock Holmes, this is my friend and colleague, Dr. Watson. You may speak freely in front of him, as he rarely understands a word.",
    "The problems of your past are your business. The problems of your future are my privilege.",
    "Dear God. What is it like in your funny little brains? It must be so boring.",
    "There is a mute button and I will use it.",
    "Every fairy tale needs a good old-fashioned villain.",
    "I'm not a psychopath, Anderson, I'm a high functioning sociopath. Do your research.",
    "Sentiment is a chemical defect found in the losing side.",
    "Get out. I need to go to my mind palace.",
    "Sometimes to solve a case, one must first solve another.",
    "Suberb, suicide as street theatre, murder by corpse. Lestrade, you're spoiling us.",
    "Come at once if convenient. If inconvenient, come all the same.",
    "It is no easy thing for a great mind to contemplate a still greater one.",
    "You must forgive Watson, he has an enthusiasm for stating the obvious, which borders on mania.",
    "You can't set a trap without bait.",
    "We all have a past, Watson. Ghosts. They are the shadows that define our every sunny day.",
    "Pure reason toppled by sheer melodrama. Your life in a nutshell.",
    "We don't need toys to kill each other. Where's the intimacy in that?",
    "It's not the fall that kills you, Sherlock. Of all people, you should know that, it's not the fall, it's never the fall. It's the landing!",
    "Nobody deceives like an addict.",
    "Controlled usage is not usually fatal and abstinence is not immortality.",
    "I'm an army doctor, which means I could break every bone in your body while naming them.",
    "Oh, good old Watson! How would we fill the time if you didn't ask questions?",
    "Once the idea exists, it cannot be killed.",
    "You know what I am. I'm Moriarty. The Napoleon of Crime.",
    "I'm a story-teller, I know when I'm in one.",
    "I've always known I was a man out of his time.",
    "I lack the arrogance to ignore details. I'm not the police.",
    "No human action is ever truly random.",
    "Work is the best antidote to sorrow.",
    "I'm very busy at the moment, I have to drink a cup of tea.",
    "Everybody dies. It's the one thing human beings can be relied upon to do. How can it still come as a surprise to people?",
    "Stress can ruin every day of your life. Dying can only ruin one.",
    "My name's Jim Moriarty. Welcome to the final problem.",
    "A nice murder. That'll cheer you up.",
    "\"It's OK.\" - \"It's not OK.\" - \"No, but it is what it is.\"",
    "https://tenor.com/view/moriarty-missme-sherlock-gif-5139409",
    "https://tenor.com/view/moriarty-king-gif-7591281",
    "https://tenor.com/view/sherlock-benedict-cumberbatch-hat-gif-15943210",
    "https://tenor.com/view/awesome-moriarty-sherlock-sherlocked-gif-7569366",

]

kaamelott_quotes = [
    "- Et va falloir vous y faire parce qu'à partir de maintenant, on va s'appeler \"Les Chevaliers de la Table Ronde\" !\n- Ben heureusement qu'on s'est pas fait construire un buffet à vaisselle !",
    "J'ai rêvé qu'il y avait des scorpions qui voulaient me piquer. En plus, y en avait un il était mi-ours, mi-scorpion et re mi-ours derrière !",
    "- C'est vrai que vous êtes le fils d'un démon et d'une pucelle ?\n- Oui pourquoi ?\n- Vous avez plus pris de la pucelle...",
    "J'irai me coucher quand vous m'aurez juré qu'il n'y a pas dans cette forêt d'animal plus dangereux que le lapin adulte !",
    "Moi j'ai appris à lire, ben je souhaite ça à personne.",
    "Vous avez été marié comme moi ; vous savez que la monstruosité peut prendre des formes diverses.",
    "- Qu'est-ce qui est petit et marron ?\n- Un marron !\n- Putain il est fort, ce con.",
    "Moi, je m'en fous, si on me force à y retourner, je retiens ma respiration jusqu'à ce qu'on arrête de me forcer à y retourner.",
    "Elle est où la poulette ?",
    "Une pluie de pierres ? En intérieur ? Ah, je vous prenais pour un pied de chaise, mais en fait vous êtes un précurseur, Monsieur !",
    "JE NE MANGE PAS DE GRAINES !!",
    "Eh bien, c'est l'histoire d'un petit ourson qui s'appelle... Arthur. Et y'a une fée, un jour, qui vient voir le petit ourson et qui lui dit : « Arthur tu vas partir à la recherche du Vase Magique ». Et elle lui donne une épée hmm... magique (ouais, parce qu'y a plein de trucs magiques dans l'histoire, bref) alors le petit ourson il se dit : « Heu, chercher le Vase Magique ça doit être drôlement difficile, alors il faut que je parte dans la forêt pour trouver des amis pour m'aider ». Alors il va voir son ami Lancelot... le cerf (parce que le cerf c'est majestueux comme ça), heu, Bohort le faisan et puis Léodagan... heu... l'ours, ouais c'est un ours aussi, c'est pas tout à fait le même ours mais bon. Donc Léodagan qui est le père de la femme du petit ourson, qui s'appelle Guenièvre la truite... non, non, parce que c'est la fille de... non c'est un ours aussi puisque c'est la fille de l'autre ours, non parce qu'après ça fait des machins mixtes, en fait un ours et une truite... non en fait ça va pas.\nBref, sinon y'a Gauvain le neveu du petit ourson qui est le fils de sa soeur Anna, qui est restée à Tintagel avec sa mère Igerne la... bah non, ouais du coup je suis obligé de foutre des ours de partout sinon on pige plus rien dans la famille... Donc c'est des ours, en gros, enfin bref... Ils sont tous là et donc Petit Ourson il part avec sa troupe à la recherche du Vase Magique. Mais il le trouve pas, il le trouve pas parce qu'en fait pour la plupart d'entre eux c'est... c'est des nazes : ils sont hyper mous, ils sont bêtes, en plus y'en a qu'ont la trouille. Donc il décide de les faire bruler dans une grange pour s'en débarrasser... Donc la fée revient pour lui dire : « Attention petit ourson, il faut être gentil avec ses amis de la forêt » quand même c'est vrai, et du coup Petit Ourson il lui met un taquet dans la tête à la fée, comme ça : « BAH ! ». Alors la fée elle est comme ça et elle s'en va... et voilà et en fait il trouve pas le vase. En fait il est... il trouve pas... et Petit Ourson il fait de la dépression et tout les jours il se demande s'il va se tuer ou... pas...",
    "- Et ils avaient des éléphants ?\n- Des éléphants ?! Non non, mais ils avaient des chevaux tout gris, tout chelous avec la queue au milieu du visage !\n- Ah oui, des éléphants...",
    "Donc, pour résumer, je suis souvent victime des colibris, sous-entendu des types qu’oublient toujours tout, euh, non... Bref, tout ça pour dire, que je voudrais bien qu’on me considère en tant que tel.",
    "Le gras c’est la vie !",
    "De toute façon, les réunions de la Table Ronde c’est deux fois par mois. Donc si le mec il dit après-demain à partir de dans deux jours, suivant s’il le dit à la fin du mois, ça reporte.",
    "Faut pas respirer la compote, ça fait tousser.",
    "PAYS DE GALLE INDÉPENDAAAAAAAAAAAAAAAAAAAANT !!!",
    "CUUUUUUUUUILLÈÈÈÈÈÈRE !!",
    "Si vous prenez aujourd’hui, que vous comptez sept jours, on retombe le même jour mais une semaine plus tard... Enfin à une vache près, c’est pas une science exacte.",
    "C’est pas moi qui explique mal, c’est les autres qui sont cons.",
    "Un engin comme vous, ça devrait être livré avec une notice !",
    "Ah, le printemps ! La nature se réveille, les oiseaux reviennent, on crame des mecs.",
    "- Ça va je vous force pas à manger des briques non plus !\n- Enfin sans vouloir me la ramener, la seule différence concrète avec des briques, c’est que vous appelez ça des tartes !",
    "Vous, vous devriez arrêter de sourire. J’vous promets ; ça devient vraiment malsain.",
    "Non mais c’est dingue cette histoire ! C’est pas parce que vous faite des tartes pour des petits enfants qui n’existent pas, que je dois les emmener à la pêche !",
    "Odi panem quid meliora. Ça veut rien dire, mais je trouve que ça boucle bien.",
    "Victoriae mundis et mundis lacrima ! Ça ne veut absolument rien dire, mais je trouve que c'est assez dans le ton",
    "Les momes, maintenant, ils lisent, ils lisent, ils lisent... Et résultat : ils sont encore puceaux à 10 ans",
    "Ces conneries de gauche et de droite ! Ça veut rien dire ces machins ! Selon comme on est tourné ça change tout !",

]
