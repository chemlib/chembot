import argparse
import chemlib
import discord
from discord.ext import commands
import cogs.utils.error

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-cmpd', type=str)

cmpd_parser = argparse.ArgumentParser(parents=[parser])
cmpd_parser.add_argument('--amount', type=str)
cmpd_parser.add_argument('--composition', type=str)

class Compounds(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.group(name = 'cmpd', aliases = ['compound', 'comp'])
    async def cmpd(self, ctx, *args):
        try:
            emoji = u"\u2705"
            cmd = vars(cmpd_parser.parse_args(['-cmpd'] + list(args)))
            compound = chemlib.Compound(cmd['cmpd'])
            embed = discord.Embed(title=f'{compound.formula} Properties', color=0x7b2fde)
            if compound.molar_mass() == 0: raise ValueError
            embed.add_field(name = "Molar Mass", value = str(compound.molar_mass()) + ' g/mol', inline=False)
            
            if cmd['amount'] is not None:
                amt = cmd['amount']
                if 'g' in amt: amts = compound.get_amounts(grams = float(amt[:-1]))
                elif 'mol' in amt: amts = compound.get_amounts(moles = float(amt[:-3]))
                else: amts = compound.get_amounts(molecules = float(amt[:-9]))
                for field in amts:
                    if field not in ('compound', 'Compound'):
                        embed.add_field(name = field.capitalize(), value=amts[field], inline=True)
            
            if cmd['composition'] is not None:
                elem = cmd['composition']
                embed.add_field(name = f"% composition of {elem}", value = compound.percentage_by_mass(elem), inline=False)
        except:
            emoji = "❌"
            embed = cogs.utils.error.Error(f"Error parsing the inputted formula.", example= "-cmpd C6H12O6\n-cmpd H2O2 --am 25g\n-cmpd AlCl3 --am 3.5mol\n-cmpd H2S --comp S")
        
        await ctx.message.add_reaction(emoji)
        await ctx.send(embed = embed)
    
def setup(bot):
    bot.add_cog(Compounds(bot))