"""Quiz class for games Cog

(C) 2021 Clément SEIJIDO
Released under GNU General Public License v3.0 (GNU GPLv3)
e-mail clement@seijido.fr
"""

import datetime
import random


class Quiz(object):
    def __init__(self):
        self.ready = False

        self.langue = None
        self.category = None
        self.theme = None
        self.difficulty = None
        self.question = None
        self.correct_answer = None
        self.other_choices = None
        self.anecdote = None
        self.wikipedia = None

        self.starting_time = None
        self.cleaned_response = None
        self.hint = False

    def start(self, api_response):
        self.langue = api_response["langue"]
        self.category = api_response["categorie"]
        self.theme = api_response["theme"]
        self.difficulty = api_response["difficulte"]
        self.question = api_response["question"]
        self.correct_answer = api_response["reponse_correcte"]
        self.other_choices = api_response["autres_choix"]
        self.anecdote = api_response["anecdote"]
        self.wikipedia = api_response["wikipedia"]

        self.cleaned_response = Quiz.clean_response(self.correct_answer)
        random.shuffle(self.other_choices)
        self.starting_time = datetime.datetime.now()
        self.hint = False
        self.ready = True

    @classmethod
    def clean_response(cls, response):
        response = response.casefold().strip()

        # remove quotes around the response if any
        if response[0] == "'":
            response = response[1:]
        if response[-1] == "'":
            response = response[:-1]

        stop_words = [
            "le",
            "la",
            "les",
            "un",
            "une",
            "des"
        ]
        response = " ".join(
            [word for word in response.split(" ") if word not in stop_words]
        )

        response = response.replace("à", "a") \
            .replace("â", "a") \
            .replace("ä", "a") \
            .replace("ç", "c") \
            .replace("é", "e") \
            .replace("è", "e") \
            .replace("ê", "e") \
            .replace("ë", "e") \
            .replace("î", "i") \
            .replace("ï", "i") \
            .replace("ô", "o") \
            .replace("ö", "o") \
            .replace("ù", "u") \
            .replace("û", "u") \
            .replace("ü", "u") \
            .replace("ÿ", "y") \
            .replace("œ", "oe") \
            .replace("’", "'")

        return response
