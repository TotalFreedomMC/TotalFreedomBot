import discord
import os
import time
import sys
import logscript
import re

from unicode import *
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from checks import *
from functions import *

print = logscript.logging.getLogger().critical

load_dotenv()
botToken = os.getenv('botToken')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.getenv('prefix'),
                   description='TotalFreedom bot help command', intents=intents)


extensions = [
    "commands.moderation",
    "commands.server_commands",
    "commands.help",
    "commands.miscellaneous",
    "commands.music",
    "events"
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(
                f"[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Extensions] {extension} loaded successfully")
        except Exception as e:
            print(
                f"[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Extensions] {extension} didn't load {e}")


@bot.event
async def on_message(message):
    if message.guild and message.author is message.guild.me and message.channel.id == reports_channel_id:
        await message.add_reaction(clipboard)
    if message.type == discord.MessageType.new_member:
        if re.search('discord\.gg\/[a-zA-z0-9\-]{1,16}', message.author.name.lower()) or re.search('discordapp\.com\/invite\/[a-z0-9]+/ig', message.author.name.lower()):
            await message.author.ban(reason="Name is an invite link.")
            await message.delete()
    bypass_roles = [discord_admin, discord_mod]
    bypass = False
    if message.author != bot.user:
        for role in message.author.roles:
            if role.id in bypass_roles:
                bypass = True
    else:
        if 'Server has started' in message.content:  # Telnet reconnect script
            try:
                bot.telnet_object.connect()
            except Exception as e:
                print(f'Failed to reconnect telnet: {e}')
                time.sleep(5)
                try:
                    bot.telnet_object.connect()
                except Exception as fuckup:
                    print(
                        f'Second attempt failed to reconnect telnet: {fuckup}')
    if not bypass:
        if re.search('discord\.gg\/[a-zA-z0-9\-]{1,16}', message.content) or re.search('discordapp\.com\/invite\/[a-z0-9]+/ig', message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention} do not post invite links to other discord servers.")

    if message.content.lower().startswith(os.getenv('prefix')):
        await bot.process_commands(message)

bot.run(botToken)
