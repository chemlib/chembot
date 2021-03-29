import chemlib
import discord
from discord.ext import commands
import cogs.utils

class Galvanic_Cells(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(name='gcell', description='Gets the general properties of a Galvanic Cell.')
    async def gcell(self, ctx, *args):
        if len(args) != 2:
            await ctx.message.add_reaction("❌")
            await ctx.send(embed = cogs.utils.error.Error("Requires two electrodes.", example="-gcell Sn Mg"))
            return
        try:
            e1, e2 = args[0], args[1]
            cell = chemlib.Galvanic_Cell(e1, e2)
            cell.diagram.save('gcell.png')
            file = discord.File('gcell.png', filename='gcell.png')
            embed = discord.Embed(title=f'{cell.anode[0]}-{cell.cathode[0]} Galvanic Cell', color=0x7b2fde)
            embed.set_image(url="attachment://gcell.png")
            await ctx.message.add_reaction(u"\u2705")
            await ctx.send(file = file, embed = embed)
        except:
            await ctx.message.add_reaction("❌")
            embed = cogs.utils.error.Error('Either one or both of the inputted electrodes is unknown or invalid.', example="-gcell Ag Pb")
            await ctx.send(embed = embed)
    
def setup(bot):
    bot.add_cog(Galvanic_Cells(bot))
