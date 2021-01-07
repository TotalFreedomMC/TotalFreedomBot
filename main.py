import os
import re
import time
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

import logscript
from functions import config_entry, get_prefix, hit_endpoint, get_server_status
from unicode import clipboard

print = logscript.logging.getLogger().critical

load_dotenv()
botToken = os.getenv('botToken')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, description='TotalFreedom bot help command',
                   intents=intents)

bot.server_liaison = config_entry("server_liaison")
bot.event_host = config_entry("event_host")
bot.server_banned = config_entry("server_banned")
bot.senior_admin = config_entry("senior_admin")
bot.admin = config_entry("admin")
bot.master_builder = config_entry("master_builder")
bot.reports_channel_id = config_entry("reports_channel_id")
bot.archived_reports_channel_id = config_entry("archived_reports_channel_id")
bot.guild_id = config_entry("guild_id")
bot.mentions_channel_id = config_entry("mentions_channel_id")
bot.discord_admin = config_entry("discord_admin")
bot.discord_mod = config_entry("discord_mod")
bot.devs = config_entry("devs")
bot.bot_logs_channel_id = config_entry("bot_logs_channel_id")
bot.executive = config_entry("executive")
bot.asst_exec = config_entry("asst_exec")
bot.developer = config_entry("developer")
bot.creative_designer = config_entry("creative_designer")
bot.server_chat = config_entry("server_chat")
bot.verification_role = config_entry("verification_role")
bot.server_chat_2 = config_entry("server_chat_2")

extensions = [
    "commands.moderation",
    "commands.server_commands",
    "commands.help",
    "commands.miscellaneous",
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
    if isinstance(message.channel, discord.channel.DMChannel):
        print(f'{message.author} DM: {message.content}')
        return
    elif message.guild and message.author is message.guild.me and message.channel.id == bot.reports_channel_id:
        await message.add_reaction(clipboard)
    elif message.type == discord.MessageType.new_member:
        if re.search('discord\.gg\/[a-zA-z0-9\-]{1,16}', message.author.name.lower()) or re.search(
                'discordapp\.com\/invite\/[a-z0-9]+/ig', message.author.name.lower()):
            await message.author.ban(reason="Name is an invite link.")
            await message.delete()
    bypass_roles = [bot.discord_admin, bot.discord_mod]
    bypass = False
    if message.author != bot.user:
        for role in message.author.roles:
            if role.id in bypass_roles:
                bypass = True
    else:
        server_chats = {1: bot.server_chat, 2: bot.server_chat_2}
        for server in range(1, len(server_chats)):
            if message.channel.id == server_chats[server]:
                if not get_server_status(server):
                    hit_endpoint('start', server)

        if 'Server has started' in message.content:  # Telnet reconnect script
            try:
                bot.telnet_object.connect()
            except Exception as err:
                print(f'Failed to reconnect telnet: {err}')
                time.sleep(5)
                try:
                    bot.telnet_object.connect()
                except Exception as fuckup:
                    print(
                        f'Second attempt failed to reconnect telnet: {fuckup}')
            try:
                bot.telnet_object_2.connect()
            except Exception as err:
                print(f'Failed to reconnect telnet 2: {err}')
                time.sleep(5)
                try:
                    bot.telnet_object_2.connect()
                except Exception as fuckup:
                    print(
                        f'Second attempt failed to reconnect telnet 2: {fuckup}')
    if not bypass:
        if re.search('discord\.gg\/[a-zA-z0-9\-]{1,16}', message.content) or re.search(
                'discordapp\.com\/invite\/[a-z0-9]+/ig', message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention} do not post invite links to other discord servers.")

    await bot.process_commands(message)


bot.run(botToken)
