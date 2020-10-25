import ast
import discord
import datetime
import os
import time
import random
import aiofiles

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
botToken = os.getenv('botToken')

bot = commands.Bot(command_prefix=os.getenv('prefix'), description='TotalFreedom bot help command')

devs = [114348811995840515, 147765181903011840]

def is_dev(ctx):
    return ctx.message.author.id in devs

extensions = [
    "commands.Moderation",
    "commands.ServerCommands"
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
