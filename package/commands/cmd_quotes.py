# quotes command for BotAToutFer
import secrets

from discord.ext import commands

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="99", help="Répond une réplique de B99")
    async def nine_nine(self, ctx):
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

        response = secrets.choice(brooklyn_99_quotes)
        await ctx.send(response)

    @commands.command(name="good_place", help="Répond une réplique de TGP")
    async def good_place(self, ctx):
        the_good_place_quotes = [
            "Everything is fine",
            "I'm telling you, Molotov cocktails work. Anytime I had a problem and I threw a Molotov cocktail, boom! Right away, I had a different problem.",
            "Not a girl",
            
        ]

        response = secrets.choice(the_good_place_quotes)
        await ctx.send(response)

    @commands.command(name="sherlock", help="Répond une réplique de Sherlock")
    async def sherlock(self, ctx):
        sherlock_quotes = [
            "I'm not an addict, I'm a user. I alleviate boredom and occasionally heighten my thought processes.",
            "Nothing made me. I made me.",
            "Bravery is by far the kindest word for stupidity.",
            "Fear is wisdom in the face of danger, it is nothing to be ashamed of.",
            "Stress can ruin everyday of your life, dying can only ruin one.",
            "Good afternoon. I am Sherlock Holmes, this is my friend and colleague, Dr. Watson. You may speak freely in front of him, as he rarely understands a word.",
            "The problems of your past are your business. The problems of your future are my privilege.",

        ]

        response = secrets.choice(sherlock_quotes)
        await ctx.send(response)
