from discord.ext import commands
import discord
import chemlib
import argparse

GREEN_TICK = u"\u2705"
client = commands.Bot(command_prefix='-', help_command=None)

with open('token.txt') as f:
    token = f.readline() 

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-cmpd', type=str)

cmpd_parser = argparse.ArgumentParser(parents=[parser])
cmpd_parser.add_argument('--amount', type=str)
cmpd_parser.add_argument('--composition', type=str)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with chemicals"))
    print(f'We have logged in as {client.user}')

@client.command(name='help', description='Gets the general properties of an element.')
async def help(ctx):
    embed = discord.Embed(title= '**ChemBot Commands**', color=0x7b2fde)
    embed.set_thumbnail(url = 'https://github.com/chemlib/chemlib/blob/master/docs/build/html/_static/logo.png?raw=true')
    _ = client.command_prefix

    cmpds = f"```\n{_}cmpd <formula>\n   --am <units>\n   --comp <elem>```"
    elems = f"```{_}elem <symbol>```"

    embed.add_field(name = '**Elements**', value=elems, inline=False)
    embed.add_field(name = '**Compounds**', value=cmpds, inline=False)

    await ctx.send(embed = embed)

@client.command(name='elem', description='Gets the general properties of an element.')
async def elem(ctx, arg):
    await ctx.message.add_reaction(GREEN_TICK)
    element = chemlib.Element(arg)
    name = element['Element']
    embed = discord.Embed(title= name, color=0x7b2fde)
    embed.set_thumbnail(url=f'https://images-of-elements.com/t/{name.lower()}.png')
    for property in ('Symbol', 'AtomicNumber', "AtomicMass", "Phase", "AtomicRadius", 'Electronegativity', 'FirstIonization', 'MeltingPoint', "BoilingPoint", 'Config', 'Discoverer', 'Year'):
        embed.add_field(name = property, value = element[property])

    embed.set_footer(text=f"Query by {ctx.author.name}")
    await ctx.send(embed = embed)

@client.command(name='cmpd', description='Gets the general properties of a compound.')
async def cmpd(ctx, *args):
    cmd = vars(cmpd_parser.parse_args(['-cmpd'] + list(args)))
    compound = chemlib.Compound(cmd['cmpd'])
    await ctx.message.add_reaction(GREEN_TICK)
    embed = discord.Embed(title=f'{compound.formula} Properties', color=0x7b2fde)
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
                
    await ctx.send(embed = embed)

client.run(str(token))