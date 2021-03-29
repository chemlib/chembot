import chemlib
import discord
from discord.ext import commands
import cogs.utils

class Elements(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.group(name='elem', aliases = ['el', 'element'], description='Gets the general properties of an element.')
    async def elem(self, ctx, arg):
        try:
            emoji = u"\u2705"
            element = chemlib.Element(arg)
            name = element['Element']
            embed = discord.Embed(title= name, color=0x7b2fde)
            embed.set_thumbnail(url=f'https://images-of-elements.com/t/{name.lower()}.png')
            for property in ('Symbol', 'AtomicNumber', "AtomicMass", "Phase", "AtomicRadius", 'Electronegativity', 'FirstIonization', 'MeltingPoint', "BoilingPoint", 'Config', 'Discoverer', 'Year'):
                embed.add_field(name = property, value = element[property])

            embed.set_footer(text=f"Query by {ctx.author.name}")
        except:
            emoji = "❌"
            embed = cogs.utils.error.Error(f"The input ({arg}) is not the symbol of a valid element.", example="-elem Cu")

        await ctx.message.add_reaction(emoji) 
        await ctx.send(embed = embed)
    
def setup(bot):
    bot.add_cog(Elements(bot))
