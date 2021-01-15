from discord.ext import commands
import discord
import chemlib
import argparse

client = commands.Bot(command_prefix='-')

with open('token.txt') as f:
    token = f.readline() 

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-cmpd', type=str)

cmpd_parser = argparse.ArgumentParser(parents=[parser])
cmpd_parser.add_argument('--amount', type=str)
cmpd_parser.add_argument('--composition', type=str)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with substances"))
    print(f'We have logged in as {client.user}')

@client.command(name='cmpd', description='Gets the general properties of a compound.')
async def cmpd(ctx, *args):
    cmd = vars(cmpd_parser.parse_args(['-cmpd'] + list(args)))
    compound = chemlib.Compound(cmd['cmpd'])
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