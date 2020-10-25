import discord

from discord.ext import commands
import datetime


server_liaison = 769659653096472634
event_host = 769659653096472629
server_banned = 769659653096472636
senior_admin = 769659653129896016
admin = 769659653121900553
master_builder = 769659653121900550

def is_staff(ctx):
    user = ctx.message.author
    for role in user.roles:
        if role.id in [admin, senior_admin]:
            return True
    return False
        
def is_liaison(ctx):
    user = ctx.message.author
    for role in user.roles:
        if role.id == server_liaison:
          return True
    return False    
            
def is_senior(ctx):
    user = ctx.message.author
    for role in user.roles:
        if role.id == senior_admin:
          return True
    return False

class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.check(is_liaison)
    async def eventhost(self, ctx, user: discord.Member):
        'Add or remove event host role - liaison only'
        eventhostrole = ctx.guild.get_role(event_host)
        if eventhostrole in user.roles:
            await user.remove_roles(eventhostrole)
            await ctx.send(f'```Succesfully took Event Host from {user.name}```')
        else:
            await user.add_roles(eventhostrole)
            await ctx.send(f'```Succesfully added Event Host to {user.name}```')
    
    @commands.command()
    @commands.check(is_staff)
    async def serverban(self, ctx, user: discord.Member):
        'Add or remove server banned role'
        serverbannedrole = ctx.guild.get_role(server_banned)
        if serverbannedrole in user.roles:
            await user.remove_roles(serverbannedrole)
            await ctx.send(f'Took Server Banned role from {user.name}')
        else:
            await user.add_roles(serverbannedrole)
            await ctx.send(f'Added Server Banned role to {user.name}')
    
    @commands.command()
    @commands.check(is_staff)
    async def start(self, ctx):
        'Not currently working'
        startEmbed = discord.Embed(description='start working out fatass')
        await ctx.send(embed=startEmbed)
        
    @commands.command()
    @commands.check(is_staff)
    async def stop(self, ctx):
        'Not currently working'
        stopEmbed = discord.Embed(description='stop being so sus')
        await ctx.send(embed=stopEmbed)
    
    @commands.command()
    @commands.check(is_senior)
    async def kill(self, ctx):
        'Not currently working'
        killEmbed = discord.Embed(description='kill youself')
        await ctx.send(embed=killEmbed)
    
    @commands.command()
    @commands.check(is_staff)
    async def restart(self, ctx):
        'Not currently working'
        restartEmbed = discord.Embed(description='cant restart a dead server idiot')
        await ctx.send(embed=restartEmbed)
    
    @commands.command()
    @commands.check(is_senior)
    async def console(self, ctx,*, command):
        'Not currently working'
        await ctx.send(f'```:[{str(datetime.datetime.utcnow().replace(microsecond=0))[11:]} INFO]: {ctx.author.name} issued server command: /{command}```')
    
    
    @commands.command(aliases=['status'])
    async def state(self, ctx):
        'Not currently working'
        await ctx.send('```The server is currently fucked.```')
        
    @commands.command()
    async def list(self, ctx):
        'Not currently working'
        onlinePlayers = discord.Embed(title='Players Online', description='fuckall mate')
        await ctx.send(embed=onlinePlayers)
    
def setup(bot):
    bot.add_cog(ServerCommands(bot))
