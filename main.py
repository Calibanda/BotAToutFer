# main.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = "oZuysjAN4lH7Hhpfcg3yCVs5D2RaWCeK"

client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

client.run(TOKEN)
