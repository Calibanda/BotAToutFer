"""Hangman class for games Cog

(C) 2021 Clément SEIJIDO
Released under GNU General Public License v3.0 (GNU GPLv3)
e-mail clement@seijido.fr
"""

import datetime
import random


class Hangman(object):
    def __init__(self, dictionary_path):
        with open(dictionary_path, "r", encoding="utf-8") as f:
            # Chose a secret word in the dictionary
            word = random.choice(f.readlines())
            self.secret_word = word.casefold().strip()

        # Creating a word with "*" that will be displayed to players
        self.visible_word = "*" * len(self.secret_word)
        # Players have 10 strokes to find the word
        self.number_stroke = 10
        # Create the list to store all the guessed letters
        self.guessed_letters = []
        # The definition of the word
        self.definition = None
        # We save the datetime of the start of the game
        self.starting_time = datetime.datetime.now()

    def get_guessed_letters(self):
        s = ""
        for letter in self.guessed_letters:
            s += f"~~{letter.upper()}~~ "
        return s

    def process_visible_word(self, user_guess):
        for i in range(len(self.secret_word)):
            # Replace the guessed letter in the visible word
            if self.secret_word[i] == user_guess:
                self.visible_word = self.visible_word[:i] \
                                    + user_guess \
                                    + self.visible_word[i + 1:]

    def drawing(self):
        if self.number_stroke == 10:
            return ""
        elif self.number_stroke == 9:
            return "___"
        elif self.number_stroke == 8:
            return " |\n |\n |\n |\n |\n_|_"
        elif self.number_stroke == 7:
            return " ____________\n |\n |\n |\n |\n |\n_|_"
        elif self.number_stroke == 6:
            return " ____________\n |/\n |\n |\n |\n |\n_|_"
        elif self.number_stroke == 5:
            return " ____________\n |/     |\n |\n |\n |\n |\n_|_"
        elif self.number_stroke == 4:
            return " ____________\n |/     |\n |      O\n |\n |\n |\n_|_"
        elif self.number_stroke == 3:
            return "____________\n |/     |\n |      O\n |      |\n |      " \
                   "|\n |\n_|_"
        elif self.number_stroke == 2:
            return "____________\n |/     |\n |      O\n |     _|_\n |      " \
                   "|\n |\n_|_"
        elif self.number_stroke == 1:
            return "____________\n |/     |\n |      O\n |     _|_\n |      " \
                   "|\n |     /\n_|_ "
        elif self.number_stroke == 0:
            return "____________\n |/     |\n |      O\n |     _|_\n |      " \
                   "|\n |     / \\ \n_|_"
