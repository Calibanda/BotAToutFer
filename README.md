# BotAToutFer
[![Python Version](https://img.shields.io/badge/python-3.6-blue?style=for-the-badge&logo=python)](https://github.com/Calibanda/BotAToutFer/)
[![Open Source? Yes!](https://img.shields.io/badge/Open%20Source%3F-Yes!-green?style=for-the-badge&logo=appveyor)](https://github.com/Calibanda/BotAToutFer/)
[![License](https://img.shields.io/github/license/Calibanda/BotAToutFer?style=for-the-badge)](https://github.com/Calibanda/BotAToutFer/blob/main/LICENSE)

The 'BotAToutFer', the Discord bot that does everything (even the coffee)

## Installation 

### Clone the repository

Clone this repository in your personal directory with the command:

```
git clone https://github.com/Calibanda/BotAToutFer.git
```

### Install needed packages

Install needed packages with:

```
pip3 install -r requirements.txt
```
You can also manualy install them:

```
pip3 install -U discord.py[voice]
pip3 install -U python-dotenv
pip3 install -U bs4
pip3 install -U youtube-dl
```

### Declare environment variable

At the source of the directory, create a file named ".env". In this file, enter the private information needed by the bot:

```
# .env
DISCORD_TOKEN= #Enter here the token of your Discord bot
WEATHER_TOKEN= #Enter here the token of your openweathermap.org api
NEWS_TOKEN= #Enter here the token of your newsapi.org api
CAT_TOKEN= #Enter here the token of your thecatapi.com api
COFFEE_URL= #Enter here the URL of your coffee pot
COFFEE_PASSWORD= #Enter here the password needed to access to your coffee URL
DICOLINK_TOKEN= #Enter here the token of the dicolink dictionnay API
```

### Create json for declaring channels bot

At the source of the directory, create a json file named "channels.json". In this file, enter channels'id in which the bot can respond to commands and send kitten picture:

```
[
    "123456789012345678": "description of the channel (not used, optionnal)",
    "876543210987654321": ""
]
```

## Running the bot

Execute the following command to start the bot:

```
python3 main.py
```
