# BotAToutFer
[![Python Version](https://img.shields.io/badge/python-3.10-blue?style=for-the-badge&logo=python)](https://github.com/Calibanda/BotAToutFer/)
[![Open Source? Yes!](https://img.shields.io/badge/Open%20Source%3F-Yes!-green?style=for-the-badge&logo=appveyor)](https://github.com/Calibanda/BotAToutFer/)
[![License](https://img.shields.io/github/license/Calibanda/BotAToutFer?style=for-the-badge)](https://github.com/Calibanda/BotAToutFer/blob/main/LICENSE)

The 'BotAToutFer', the Discord bot that does (or did) everything (even the coffee).

## Installation

### Clone the repository

Clone this repository in your personal directory with the command:

```bash
git clone https://github.com/Calibanda/BotAToutFer.git
```

### Create a new virtual environment

On Linux or MacOS

```bash
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/python3 -m pip install --upgrade pip
```

On Windows

```shell
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
```

*For more information about virtual environments see the [official documentation](https://docs.python.org/3/library/venv.html).*

### Follow installation of py-cord

Follow the installation of the Pycord library on https://github.com/Pycord-Development/pycord
    
### Install needed packages

Install needed packages with:

```bash
pip install -r requirements.txt
```

List of direct dependencies:

- python-dotenv
- py-cord
- yt-dlp

### Declare environment variable

At the source of the directory, create a file named ".env". In this file, enter the private information needed by the bot:

```
# .env
DISCORD_TOKEN= #Enter here the token of your Discord bot
OWNER_IDS= #Enter here the IDS of the bot owners (separated by a semicolon)
DEBUG_GUILDS= #Enter here the IDS of the debug guilds if any (separated by a semicolon)
```

## Running the bot

Execute the following command to start the bot:

```bash
python main.py
```
