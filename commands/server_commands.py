import discord
import requests
import re
import time

from checks import *
from discord.ext import commands
from datetime import datetime
from functions import *
from unicode import clipboard


class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def write_telnet_session(self, server, to_write):
        if server == 1:
            return self.bot.telnet_object.session.write(to_write)
        else:
            return self.bot.telnet_object_2.session.write(to_write)
    
    def read_until_telnet(self, to_read, server):
        if server == 1:
            return self.bot.telnet_object.session.read_until(to_read).decode('utf-8')
        else:
            return self.bot.telnet_object_2.session.read_until(to_read).decode('utf-8')
            
    @commands.command()
    @is_liaison()
    async def eventhost(self, ctx, user: discord.Member):
        """Add or remove event host role - liaison only."""
        eventhostrole = ctx.guild.get_role(event_host)
        if eventhostrole in user.roles:
            await user.remove_roles(eventhostrole)
            await ctx.send(f'```Succesfully took {eventhostrole.name} from {user.name}```')
        else:
            await user.add_roles(eventhostrole)
            await ctx.send(f'```Succesfully added {eventhostrole.name} to {user.name}```')

    @commands.command()
    @is_creative_designer()
    async def masterbuilder(self, ctx, user: discord.Member):
        """Add or remove master builder role - ECD only."""
        master_builder_role = ctx.guild.get_role(master_builder)
        if master_builder_role in user.roles:
            await user.remove_roles(master_builder_role)
            await ctx.send(f'```Succesfully took {master_builder_role.name} from {user.name}```')
        else:
            await user.add_roles(master_builder_role)
            await ctx.send(f'```Succesfully added {master_builder_role.name} to {user.name}```')

    @commands.command()
    @is_staff()
    async def serverban(self, ctx, user: discord.Member):
        """Add or remove server banned role."""
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
        """Starts the server."""
        em = discord.Embed()
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        try:
            attempt = hit_endpoint('start', server)
        except Exception as e:
            em.title = 'Command error'
            em.colour = 0xFF0000
            em.description = 'Something went wrong'
            print(f'Error while starting server: {e}')
            await ctx.send(embed=em)
        else:
            if 'error' in attempt.lower():
                em.title = 'Command error'
                em.colour = 0xFF0000
                em.description = f'{attempt}'
                await ctx.send(embed=em)
            else:
                em.title = 'Success'
                em.colour = 0x00FF00
                em.description = f'{attempt}'
                await ctx.send(embed=em)

    @commands.command()
    async def uptime(self, ctx):
        """Returns the uptime of the VPS."""
        em = discord.Embed()
        em.title = 'VPS Uptime Information'
        em.description = hit_endpoint('uptime')
        await ctx.send(embed=em)

    @commands.command()
    @is_staff()
    async def stop(self, ctx):
        """Stops the server."""
        em = discord.Embed()
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        try:
            attempt = hit_endpoint('stop', server)
        except Exception as e:
            em.title = 'Command error'
            em.colour = 0xFF0000
            em.description = 'Something went wrong'
            print(f'Error while stopping server: {e}')
            await ctx.send(embed=em)
        else:
            if 'error' in attempt.lower():
                em.title = 'Command error'
                em.colour = 0xFF0000
                em.description = f'{attempt}'
                await ctx.send(embed=em)
            else:
                em.title = 'Success'
                em.colour = 0x00FF00
                em.description = f'{attempt}'
                await ctx.send(embed=em)

    @commands.command(aliases=['adminconsole', 'ac'])
    @is_staff()
    async def telnet(self, ctx, *args):
        """mv, gtfo, kick, mute or warn from discord."""
        em = discord.Embed()
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        command = ''
        for arg in args:
            command += f'{arg} '
        try:
            if args[0] in ['mute', 'stfu', 'gtfo', 'ban', 'unban', 'unmute', 'smite', 'noob', 'tban', 'tempban', 'warn', 'mv', 'kick', 'cc', 'say']:
                self.write_telnet_session(server, 
                    bytes(command, 'ascii') + b"\r\n")
            elif args[0] == 'saconfig':
                if args[1] not in ['add', 'remove']:
                    raise no_permission(['IS_SENIOR_ADMIN'])
                else:
                    self.write_telnet_session(server, 
                        bytes(command, 'ascii') + b"\r\n")
            else:
                raise no_permission(['IS_SENIOR_ADMIN'])
        except Exception as e:
            em.title = 'Command error'
            em.colour = 0xFF0000
            em.description = f'{e}'
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = 'Command sent.'
            await ctx.send(embed=em)

    @commands.command()
    @is_senior()
    async def kill(self, ctx):
        """Kills the server."""
        em = discord.Embed()
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        try:
            attempt = hit_endpoint('kill', server)
        except Exception as e:
            em.title = 'Command error'
            em.colour = 0xFF0000
            em.description = 'Something went wrong'
            print(f'Error while killing server: {e}')
            await ctx.send(embed=em)
        else:
            if 'error' in attempt.lower():
                em.title = 'Command error'
                em.colour = 0xFF0000
                em.description = '{attempt}'
                print(f'Error while killing server: {e}')
                await ctx.send(embed=em)
            else:
                em.title = 'Success'
                em.colour = 0x00FF00
                em.description = f'{attempt}'
                await ctx.send(embed=em)

    @commands.command()
    @is_staff()
    async def restart(self, ctx):
        """Restarts the server."""
        em = discord.Embed()
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        try:
            self.write_telnet_session(server, 
                bytes('restart', 'ascii') + b"\r\n")
        except Exception as e:
            em.title = 'Command error'
            em.colour = 0xFF0000
            em.description = 'Something went wrong'
            print(f'Error while restarting server: {e}')
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = 'Server restarting.'
            await ctx.send(embed=em)

    @commands.command()
    @is_senior()
    async def console(self, ctx, *, command):
        """Send a command as console."""
        em = discord.Embed()
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        try:
            self.write_telnet_session(server, 
                bytes(command, 'ascii') + b"\r\n")
        except Exception as e:
            em.title = 'Command error'
            em.colour = 0xFF0000
            em.description = f'{e}'
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = 'Command sent.'
            await ctx.send(embed=em)

    @commands.command(aliases=['status'])
    async def state(self, ctx):
        """Gets the current status of the Server."""
        em = discord.Embed()
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        if get_server_status(server):
            em.description = 'Server is online'
            em.colour = 0x00FF00
        else:
            em.description = 'Server is offline'
            em.colour = 0xFF0000
        await ctx.send(embed=em)

    @commands.command(name='list', aliases=['l','who','lsit'])
    async def online(self, ctx):
        """Gives a list of online players."""
        em = discord.Embed()
        em.title = "Player List"
        config_file = read_json('config')
        if ctx.channel.id == 793632795598913546:
            ip = config_file['SERVER_IP_2']
        else:
            ip = config_file['SERVER_IP']
        port = config_file['PLAYERLIST_PORT']
        try:
            json = requests.get(f"http://{ip}:{port}/list?json=true", timeout=5).json()
            if json["online"] == 0:
                em.description = "There are no online players"
            else:
                em.description = f"There are {json['online']} / {json['max']} online players"
                ranks = list(json.keys())
                
                entries = []
                
                for rank in ranks:
                    if rank not in ['max', 'online'] and json[rank]:
                        rank_fixed = rank.split('_')
                        for word in range(len(rank_fixed)):
                            rank_fixed[word] = rank_fixed[word].capitalize()
                        entries.append(format_list_entry(em, json[rank], f'{" ".join(rank_fixed)}'))
                
                order = ['Owners', 'Executives', 'Developers', 'Senior Admins', 'Admins', 'Master Builders', 'Operators', 'Imposters']
                sorted = [entry for rank in order for entry in entries if entry.name == rank]
                
                for x in sorted:
                    em.add_field(name=f'{x.name} ({x.playercount})', value=x.value, inline=False)
                
        except Exception as e:
            em.description = 'Server is offline'
            print(e)
        await ctx.send(embed=em)

    @commands.command()
    async def ip(self, ctx):
        """Returns the server IP."""
        await ctx.send(embed=discord.Embed(description='play.totalfreedom.me', title='Server IP'))
        # pass #discordSRV responds already.

    @commands.command()
    @is_staff()
    async def archivereports(self, ctx):
        """Archive all in-game reports older than 24 hours."""
        count = 0
        reports_channel = self.bot.get_channel(reports_channel_id)
        archived_reports_channel = self.bot.get_channel(
            archived_reports_channel_id)
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
    
    @commands.command(aliases=['lag', 'gc'])
    async def tps(self, ctx):
        """Lag information regarding the server."""
        em = discord.Embed()
        em.title = 'Server lag information'
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        if get_server_status(server):
            self.write_telnet_session(server,
                        bytes('lag', 'ascii') + b"\r\n")
            self.read_until_telnet(
                    bytes('Uptime:', 'ascii'), server)
            server_uptime = self.read_until_telnet(
                    bytes('Current TPS =', 'ascii'), server)
            server_tps = self.read_until_telnet(
                    bytes('Maximum memory: ', 'ascii'), server)
            maximum_memory = self.read_until_telnet(
                    bytes('Allocated memory:', 'ascii'), server)
            allocated_memory = self.read_until_telnet(
                    bytes('Free memory:', 'ascii'), server)
            free_memory = self.read_until_telnet(
                    bytes('World "world":', 'ascii'), server)
            
            server_uptime = server_uptime.strip(':Current TPS =')
            server_tps = server_tps.strip(':Maximum memory:')
            maximum_memory = maximum_memory.strip(':Allocated memory:')
            allocated_memory = allocated_memory.strip(':Free memory:')
            free_memory = free_memory.strip(':World "world":')
            
            print(f'TPS: {server_tps} UPTIME: {server_uptime} MAX MEM: {maximum_memory} ALLCTD MEM: {allocated_memory} FREE MEM: {free_memory}')
            
            try:
                server_uptime = re.match('([0-9]+ days? )?([0-9]+ hours )?([0-9]+ minutes )?([0-6]?[0-9] seconds)', server_uptime)[0]
                server_tps = re.match('[0-2][0-9].?[0-9]*', server_tps)[0]
                maximum_memory = re.match('[0-9]+,?[0-9]* MB', maximum_memory)[0]
                allocated_memory = re.match('[0-9]+,?[0-9]* MB', allocated_memory)[0]
                free_memory = re.match('[0-9]+,?[0-9]* MB', free_memory)[0]
            except Exception as e:
                em.description = f'Something went wrong: {e}'
                em.colour = 0xFF0000
            else:
                em.add_field(name='TPS', value = server_tps, inline=False)
                em.add_field(name='Uptime', value = server_uptime, inline=False)
                em.add_field(name='Maximum Memory', value = maximum_memory, inline=False)
                em.add_field(name='Allocated Memory', value = allocated_memory, inline=False)
                em.add_field(name='Free Memory', value = free_memory, inline=False)
        else:
            em.description = 'Server is offline'
        await ctx.send(embed=em)
        
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
