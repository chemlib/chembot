from discord.ext import commands
import chemlib

client = commands.Bot(command_prefix='-')
with open('token.txt') as f:
    token = f.readline() 

@client.command(name='mass', description='Gets the molar mass of specified compound.')
async def mass(ctx, cmpd):
    try: msg = str(chemlib.Compound(cmpd).molar_mass())
    except Exception as e: msg = str(e)
    await ctx.send(msg)

client.run(str(token))