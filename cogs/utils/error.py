import discord

def Error(msg: str, title = "An error occured.", color=0xd43817, example = None) -> discord.Embed:
    embed = discord.Embed(title= title, description=msg, color=color)
    if example is not None:
        embed.add_field(name = "Example", value=example)
    return embed