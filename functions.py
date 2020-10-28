import discord

from discord.ext import commands
from checks import *

def format_list_entry(embed, list, name):
    embed.add_field(name="{} ({})".format(name, len(list)), value=", ".join(list), inline=False)
    return embed

async def fix_reports():
    reports_channel = bot.get_channel(reports_channel_id)
    messages = await reports_channel.history(limit=500).flatten()
    fixed = 0
    for message in messages:
        if len(message.reactions) == 0 and message.author == message.guild.me:
            await message.add_reaction(clipboard)
            fixed += 1
    return fixed

def get_avatar(user, animate=True):
    if user.avatar_url:
        avatar = str(user.avatar_url).replace(".webp", ".png")
    else:
        avatar = str(user.default_avatar_url)
    if not animate:
        avatar = avatar.replace(".gif", ".png")
    return avatar