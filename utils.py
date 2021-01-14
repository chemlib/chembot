import discord

def build_embed(title: str, desc = "", color=0x7b2fde, fields = ()) -> discord.Embed:
    embed = discord.Embed(title=title, description=desc, color=color)
    for field in fields:
        embed.add_field(name = field[0], value = field[1], inline = False)

    return embed