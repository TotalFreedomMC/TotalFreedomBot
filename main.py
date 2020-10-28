import ast
import discord
import datetime
import os
import time
import random
import aiofiles
import re

from unicode import *
from discord.ext import commands
from dotenv import load_dotenv
from checks import *
from functions import *

load_dotenv()
botToken = os.getenv('botToken')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.getenv('prefix'), description='TotalFreedom bot help command', intents=intents)

extensions = [
    "commands.Moderation",
    "commands.Server Commands",
    "commands.help",
    "commands.Miscellaneous"
]



if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Extensions] {extension} loaded successfully")
        except Exception as e:
            print("[{} INFO]: [Extensions] {} didn't load {}".format(datetime.datetime.utcnow().replace(microsecond=0), extension, e))


@bot.event
async def on_ready():
    bot.reaction_roles = []
    
    for file in ['reactionroles.txt']:
        async with aiofiles.open(file, mode='a') as temp:
            pass
    async with aiofiles.open('reactionroles.txt', mode='r') as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(' ')
            bot.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip('\n')))
    
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Client] {bot.user.name} is online.')
    game = discord.Game('play.totalfreedom.me')
    await bot.change_presence(status=discord.Status.online, activity=game)

    guildCount = len(bot.guilds)
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Guilds] Bot currently in {guildCount} guilds.')
    for guild in bot.guilds:
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Guilds] Connected to guild: {guild.name}, Owner: {guild.owner}')
    global starttime
    starttime = datetime.datetime.utcnow()
 
def did_mention_other_user(users, author):
    for user in users:
        if user is not author:
            return True
    return False

def removed_user_mentions(old, new):
    users = []
    for user in old:
        if user not in new:
            users.append(user)
    return users

def removed_role_mentions(old, new):
    roles = []
    for role in old:
        if role not in new:
            roles.append(role)
    return roles

def get_avatar(user, animate=True):
    if user.avatar_url:
        avatar = str(user.avatar_url).replace(".webp", ".png")
    else:
        avatar = str(user.default_avatar_url)
    if not animate:
        avatar = avatar.replace(".gif", ".png")
    return avatar

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
    for role in message.author.roles:
        if role.id in bypass_roles:
            bypass = True
    if not bypass:
        if re.search('discord\.gg\/[a-zA-z0-9\-]{1,16}', message.content) or re.search('discordapp\.com\/invite\/[a-z0-9]+/ig', message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention} do not post invite links to other discord servers.")
            return
    await bot.process_commands(message)
    
@bot.event
async def on_message_edit(before, after):
    if not isinstance(before.author, discord.Member):
        return
    if before.guild.id != guild_id\
            :
        return
    users = removed_user_mentions(before.mentions, after.mentions)
    roles = removed_role_mentions(before.role_mentions, after.role_mentions)
    if users:
        users = ", ".join([str(member) for member in users])
    if roles:
        roles = ", ".join([role.name for role in roles])
    if not users and not roles:
        return
    embed = discord.Embed(description="In {}".format(before.channel.mention))
    if users:
        embed.add_field(name="Users", value=users, inline=True)
    if roles:
        embed.add_field(name="Roles", value=roles, inline=True)
    embed.color = 0xFF0000
    embed.title = "Message Edit"
    embed.set_footer(text=str(before.author), icon_url=get_avatar(before.author))
    channel = before.guild.get_channel(mentions_channel_id)
    await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if not isinstance(message.author, discord.Member):
        return
    if message.guild.id != guild_id:
        return
    users = None
    roles = None
    if did_mention_other_user(message.mentions, message.author):
        users = ", ".join([str(member) for member in message.mentions])
    if message.role_mentions:
        roles = ", ".join([role.name for role in message.role_mentions])
    if not users and not roles:
        return
    embed = discord.Embed(description="In {}".format(message.channel.mention))
    if users is not None:
        embed.add_field(name="Users", value=users, inline=True)
    if roles is not None:
        embed.add_field(name="Roles", value=roles, inline=True)
    embed.color = 0xFF0000
    embed.title = "Message Deletion"
    embed.set_footer(text=str(message.author), icon_url=get_avatar(message.author))
    channel = message.guild.get_channel(mentions_channel_id)
    await channel.send(embed=embed) 


@bot.event
async def on_command_error(ctx, error):
    await ctx.send('''```py
{}```'''.format(error))
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Commands] {ctx.author} failed running: {ctx.message.content} in guild: {ctx.guild.name}')

@bot.event
async def on_command_completion(ctx):
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Commands] {ctx.author} ran: {ctx.message.content} in guild: {ctx.guild.name}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member == bot.user:
        pass
    else:
        for role_id, msg_id, emoji in bot.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode('utf-8')):
                await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(role_id), reason='reaction')
        if payload.channel_id == reports_channel_id:
            guild = bot.get_guild(guild_id)
            reports_channel = bot.get_channel(reports_channel_id)
            report = await reports_channel.fetch_message(payload.message_id)
            if report.author == guild.me:
                if payload.emoji.name == clipboard:
                    await report.add_reaction(confirm)
                    await report.add_reaction(cancel)
                elif payload.emoji.name == cancel:
                    await report.clear_reactions()
                    await report.add_reaction(clipboard)
                elif payload.emoji.name == confirm:
                    embed = report.embeds[0]
                    archived_reports_channel = bot.get_channel(archived_reports_channel_id)
                    await report.delete()
                    await archived_reports_channel.send("Handled by " + guild.get_member(payload.user_id).mention, embed=embed)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.member == bot.user:
        pass
    else:
        for role_id, msg_id, emoji in bot.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode('utf-8')):
                await bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(bot.get_guild(payload.guild_id).get_role(role_id), reason='reaction')
            

bot.run(botToken)