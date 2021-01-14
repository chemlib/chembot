from discord.ext import commands
import chemlib
import utils

client = commands.Bot(command_prefix='#')

with open('token.txt') as f:
    token = f.readline() 

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(name='mass', description='Gets the molar mass of specified compound.')
async def mass(ctx, arg):
    cmpd = chemlib.Compound(arg)
    embed = utils.build_embed(
        title = 'Molar Mass Calculator',
        fields = [("Compound", arg), 
                  ("Mass", f"{cmpd.molar_mass()} g/mol")
                 ]
    )
    await ctx.send(embed = embed)

@client.command(name='compound', description='Gets the general properties of a compound.')
async def mass(ctx, arg):
    cmpd = chemlib.Compound(arg)
    embed = utils.build_embed(
        title = f'{cmpd.formula} Properties',
        fields = [("Mass", f"{cmpd.molar_mass()} g/mol")
                 ]
    )
    await ctx.send(embed = embed)

client.run(str(token))