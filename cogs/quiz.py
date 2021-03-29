import discord
from discord.ext import commands
from cogs.utils.error import Error
import reader, random

SUBJECTS = ['ASTRONOMY', 'BIOLOGY', 'CHEMISTRY', 'EARTH AND SPACE', 'ENERGY', 'PHYSICS']

class Quiz(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(name='quiz', description='Science quiz.')
    async def quiz(self, ctx, arg: str = None):
        def check(author):
            def inner_check(message):
                return message.author == author
            return inner_check

        if arg is None:
            q = reader.random_question(random.choice(SUBJECTS))
        else:
            selected = None
            for s in SUBJECTS:
                if arg.upper() in s:
                    selected = s
            try:
                q = reader.random_question(selected)
            except:
                q = reader.random_question(random.choice(SUBJECTS))

        author = ctx.message.author
        ans = q['Answer']
        desc = ""
        for opt in ('W', 'X', 'Y', 'Z'): 
            desc += f"**{opt}.** " + q['Options'][opt] + '\n'
        embed = discord.Embed(title = q['Question'], description=desc, color=0x7b2fde)
        embed.set_footer(text = q['Subject'])
        await ctx.send(embed = embed)
        tries = 0
        while True:
            try:
                msg = await self.bot.wait_for('message', check=check(author), timeout=20 - tries*5)
                tries += 1
                if str(msg.content).upper() != ans:
                    await msg.add_reaction("❌")
                else:
                    await msg.add_reaction(u"\u2705")
                    embed = Error(f"The correct answer was {ans}.", title = "Well done!", color = 0x5bdb21)
                    embed.set_footer(text = f"Answered by {author}")
                    await ctx.send(embed = embed)
                    break
            except:
                embed = Error(f"The correct answer was {ans}.", title="Time's up!")
                embed.set_footer(text = author)
                await ctx.send(embed = embed)
                break
    
def setup(bot):
    bot.add_cog(Quiz(bot))
