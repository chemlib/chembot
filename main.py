from discord.ext import commands
import chemlib
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# client = discord.Client()

client = commands.Bot(command_prefix='-')


@client.command(name='mass', description='Gets the molar mass of specified compound.')
async def mass(ctx, cmpd):
    try: msg = str(chemlib.Compound(cmpd).molar_mass())
    except Exception as e: msg = str(e)
    await ctx.send(msg)

client.run(TOKEN)
