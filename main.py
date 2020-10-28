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

load_dotenv()
botToken = os.getenv('botToken')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=os.getenv('prefix'), description='TotalFreedom bot help command', intents=intents)

devs = [114348811995840515, 147765181903011840]

def is_dev(ctx):
    return ctx.message.author.id in devs

extensions = [
    "commands.Moderation",
    "commands.ServerCommands"
]

guild_id = 769659653096472627
mentions_channel_id = 769659654027739151
server_liaison = 769659653096472634
event_host = 769659653096472629
server_banned = 769659653096472636
senior_admin = 769659653129896016
admin = 769659653121900553
master_builder = 769659653121900550
reports_channel_id = 769659654791233585
archived_reports_channel_id = 769659655033978900
discord_admin = 769659653129896025
discord_mod = 769659653129896023

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

@bot.command()
@commands.has_permissions(manage_roles=True)
async def setreaction(ctx, role : discord.Role=None, msg : discord.Message=None, emoji=None):
    if role and msg and emoji :
        await msg.add_reaction(emoji)
        bot.reaction_roles.append((role.id,msg.id,str(emoji.encode('utf-8'))))
        
        async with aiofiles.open("reactionroles.txt", mode='a') as file:
            emoji_utf = emoji.encode('utf-8')
            await file.write(f'{role.id} {msg.id} {emoji_utf}\n')
            
@bot.command()
async def ip(ctx):
    'Returns the server IP'
    await ctx.send('play.totalfreedom.me')
   # pass # discordSRV responds already.    
def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

async def fix_reports():
    reports_channel = bot.get_channel(reports_channel_id)
    messages = await reports_channel.history(limit=500).flatten()
    fixed = 0
    for message in messages:
        if len(message.reactions) == 0 and message.author == message.guild.me:
            await message.add_reaction(clipboard)
            fixed += 1
    return fixed

@bot.command(pass_context=True)
@commands.check(is_dev)
async def killbot(ctx):
    await ctx.send(f'Bot offline.')
    await bot.logout()

@bot.command(name='debug')
@commands.check(is_dev)
async def debug(ctx, *, cmd):
    #Evaluates input.
    #Input is interpreted as newline seperated statements.
    #If the last statement is an expression, that is the return value.
    #Usable globals:
    #  - `bot`: the bot instance
    #  - `discord`: the discord module
    #  - `commands`: the discord.ext.commands module
    #  - `ctx`: the invokation context
    #  - `__import__`: the builtin `__import__` function
    #Such that `>eval 1 + 1` gives `2` as the result.
    #The following invokation will cause the bot to send the text '9'
    #to the channel of invokation and return '3' as the result of evaluating
    #>eval ```
    #a = 1 + 2
    #b = a * 2
    #await ctx.send(a + b)
    #a
    #```
    
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    if result is not None:
        await ctx.send(f'''```py
{result}```''')

bot.run(botToken)
