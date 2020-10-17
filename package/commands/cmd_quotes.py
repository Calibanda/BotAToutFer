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
