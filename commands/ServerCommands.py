import discord

from discord.ext import commands
from datetime import datetime
import requests

server_liaison = 769659653096472634
event_host = 769659653096472629
server_banned = 769659653096472636
senior_admin = 769659653129896016
admin = 769659653121900553
master_builder = 769659653121900550
reports_channel_id = 769659654791233585
archived_reports_channel_id = 769659655033978900


def format_list_entry(embed, list, name):
    embed.add_field(name="{} ({})".format(name, len(list)), value=", ".join(list), inline=False)
    return embed

class no_permission(commands.MissingPermissions):
    pass
    
def is_staff():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id in [admin, senior_admin]:
                return True
        else:
            raise no_permission(['IS_STAFF_MEMBER'])
    return commands.check(predicate)
   
def is_liaison():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == server_liaison:
              return True
        else:
            raise no_permission(['IS_SERVER_LIAISON'])  
    return commands.check(predicate)
     
def is_senior():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == senior_admin:
              return True
        else:
            raise no_permission(['IS_SENIOR_ADMIN'])
    return commands.check(predicate)

class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @is_liaison()
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
    @is_staff()
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
    @is_staff()
    async def start(self, ctx):
        'Not currently working'
        startEmbed = discord.Embed(description='start working out fatass')
        await ctx.send(embed=startEmbed)
        
    @commands.command()
    @is_staff()
    async def stop(self, ctx):
        'Not currently working'
        stopEmbed = discord.Embed(description='stop being so sus')
        await ctx.send(embed=stopEmbed)
    
    @commands.command()
    @is_senior()
    async def kill(self, ctx):
        'Not currently working'
        killEmbed = discord.Embed(description='kill youself')
        await ctx.send(embed=killEmbed)
    
    @commands.command()
    @is_staff()
    async def restart(self, ctx):
        'Not currently working'
        restartEmbed = discord.Embed(description='cant restart a dead server idiot')
        await ctx.send(embed=restartEmbed)
    
    @commands.command()
    @is_senior()
    async def console(self, ctx,*, command):
        'Not currently working'
        await ctx.send(f'```:[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: {ctx.author.name} issued server command: /{command}```')
    
    
    @commands.command(aliases=['status'])
    async def state(self, ctx):
        'Gets the current status of the Server'
        em = discord.Embed()
        try: 
            json = requests.get("http://play.totalfreedom.me:28966/list?json=true").json()
            em.description = 'Server is online'
        except ConnectionError:
            em.description = 'Server is offline'
        await ctx.send(embed=em)
        
    @commands.command()
    async def list(self, ctx):
        'Gives a list of online players.'
        em = discord.Embed()
        em.title = "Player List"
        try: 
            json = requests.get("http://play.totalfreedom.me:28966/list?json=true").json()
        except ConnectionError:
            em.description = 'Server is offline'
        else:
            if json["online"] == 0:
                em.description = "There are no online players"
            else:
                em.description = "There are {} / {} online players".format(json["online"], json["max"])
                owners = json["owners"]
                if len(owners) != 0:
                    em = format_list_entry(em, owners, "Server Owners")
                executives = json["executives"]
                if len(executives) != 0:
                    em = format_list_entry(em, executives, "Executives")
                developers = json["developers"]
                if len(developers) != 0:
                    em = format_list_entry(em, developers, "Developers")
                senior_admins = json["senioradmins"]
                if len(senior_admins) != 0:
                    em = format_list_entry(em, senior_admins, "Senior Admins")
                admins = json["admins"]
                if len(admins) != 0:
                    em = format_list_entry(em, admins, "Admins")
                #trialadmins = json["trialadmins"]
                #if len(trialadmins) != 0:
                    #em = format_list_entry(em, trialmods, "Trial Mods")
                masterbuilders = json["masterbuilders"]
                if len(masterbuilders) != 0:
                    em = format_list_entry(em, masterbuilders, "Master Builders")
                operators = json["operators"]
                if len(operators) != 0:
                    em = format_list_entry(em, operators, "Operators")
                imposters = json["imposters"]
                if len(imposters) != 0:
                    em = format_list_entry(em, imposters, "Imposters")
        await ctx.send(embed=em)
        
    @commands.command()
    @is_staff()
    async def archivereports(self, ctx):
        """Archive all in-game reports older than 24 hours"""
        count = 0
        reports_channel = self.bot.get_channel(reports_channel_id)
        archived_reports_channel = self.bot.get_channel(archived_reports_channel_id)
        await ctx.channel.trigger_typing()
        async for report in reports_channel.history(limit=100):
            try:
                embed = report.embeds[0]
            except:
                await report.delete()
            time = embed.timestamp
            difference = datetime.now() - time
            if difference.days >= 0:
                await report.delete()
                await archived_reports_channel.send("Message archived because it is older than 24 hours", embed=embed)
                count += 1
        await ctx.send("Archived **{}** reports that are older than 24 hours".format(count))
    
def setup(bot):
    bot.add_cog(ServerCommands(bot))
