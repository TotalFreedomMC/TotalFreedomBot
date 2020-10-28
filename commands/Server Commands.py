import discord

from checks import *
from discord.ext import commands
from datetime import datetime
import requests
from functions import fix_reports, format_list_entry

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
    async def ip(self, ctx):
        'Returns the server IP'
        await ctx.send('play.totalfreedom.me')
        #pass # discordSRV responds already.    
   
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
    
    @commands.command()
    @is_mod_or_has_perms()
    async def fixreports(self, ctx):
        await ctx.channel.trigger_typing()
        reports_channel = self.bot.get_channel(reports_channel_id)
        messages = await reports_channel.history(limit=500).flatten()
        fixed = 0
        for message in messages:
            if len(message.reactions) == 0 and message.author == message.guild.me:
                await message.add_reaction(clipboard)
                fixed += 1
        await ctx.send(f'Fixed **{fixed}** reports')

def setup(bot):
    bot.add_cog(ServerCommands(bot))