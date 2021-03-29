import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='-', case_insensitive = True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with chemicals"))
    print("We have logged in as", bot.user)

EXTENSIONS = [
    'cogs.element',
    'cogs.compound',
    'cogs.galvanic_cell',
    'cogs.quiz'
]

for extension in EXTENSIONS:
    bot.load_extension(extension)

with open('token.txt', 'r') as f:
    token = f.read()

bot.run(token)