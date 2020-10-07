# main.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #TOKEN = "NzYzNDE2NDI1ODQyODY4MjI2.X33Y8w.oD0xhHO4owXBvP3fiwl1ztqtrhs"

client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

client.run(TOKEN)
