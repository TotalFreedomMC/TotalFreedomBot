import re
from datetime import datetime

import discord
import requests
from discord.ext import commands

from checks import is_liaison, is_staff, is_senior, is_creative_designer, is_mod_or_has_perms, NoPermission, is_dev, \
    is_gmod_owner, is_smp_owner, notAdminCommand
from functions import hit_endpoint, get_server_status, format_list_entry, read_json, get_visible_player_count
from unicode import clipboard


class ServerCommands(commands.Cog, name="Server Commands"):
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
        eventhostrole = ctx.guild.get_role(self.bot.event_host)
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
        master_builder_role = ctx.guild.get_role(self.bot.master_builder)
        if master_builder_role in user.roles:
            await user.remove_roles(master_builder_role)
            await ctx.send(f'```Succesfully took {master_builder_role.name} from {user.name}```')
        else:
            await user.add_roles(master_builder_role)
            await ctx.send(f'```Succesfully added {master_builder_role.name} to {user.name}```')

    @commands.command()
    @is_gmod_owner()
    async def gmodstaff(self, ctx, user: discord.Member):
        """Add or remove GMOD Staff role - Manager only."""
        gmodstaff_role = ctx.guild.get_role(self.bot.gmodstaff_role_id)
        if gmodstaff_role in user.roles:
            await user.remove_roles(gmodstaff_role)
            await ctx.send(f'```Succesfully took {gmodstaff_role.name} from {user.name}```')
        else:
            await user.add_roles(gmodstaff_role)
            await ctx.send(f'```Succesfully added {gmodstaff_role.name} to {user.name}```')

    @commands.command()
    @is_smp_owner()
    async def smpstaff(self, ctx, user: discord.Member):
        """Add or remove SMP Staff role - Manager only."""
        smpstaff_role = ctx.guild.get_role(self.bot.smpstaff_role_id)
        if smpstaff_role in user.roles:
            await user.remove_roles(smpstaff_role)
            await ctx.send(f'```Succesfully took {smpstaff_role.name} from {user.name}```')
        else:
            await user.add_roles(smpstaff_role)
            await ctx.send(f'```Succesfully added {smpstaff_role.name} to {user.name}```')

    @commands.command()
    @is_staff()
    async def serverban(self, ctx, user: discord.Member):
        """Add or remove server banned role."""
        serverbannedrole = ctx.guild.get_role(self.bot.server_banned)
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
            print(f'Error while starting freedom-0{server}: {e}')
            await ctx.send(embed=em)
        else:
            if 'error' in attempt.lower():
                em.title = 'Command error'
                em.colour = 0xFF0000
                em.description = f'freedom-0{server}: {attempt}'
                await ctx.send(embed=em)
            else:
                em.title = 'Success'
                em.colour = 0x00FF00
                em.description = f'freedom-0{server}: {attempt}'
                await ctx.send(embed=em)

    @commands.command()
    async def uptime(self, ctx):
        """Returns the uptime of the VPS."""
        em = discord.Embed()
        em.title = 'VPS Uptime Information'
        try:
            attempt = hit_endpoint('uptime')
        except Exception as e:
            em.title = 'Command error'
            em.colour = 0xFF0000
            print(f'Error while getting VPS Uptime: {e}')
            em.description = f'Something went wrong'
        else:
            em.description = attempt
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
            tempem = discord.Embed()
            tempem.title = "Command sending"
            tempem.description = "Please stand by this could take a minute"
            tempem.colour = 0xFFFF00
            tempm = await ctx.send(embed=tempem)
            attempt = hit_endpoint('stop', server, timeout=30)
        except Exception as e:
            await tempm.delete()
            em.title = 'Command error'
            em.colour = 0xFF0000
            em.description = 'Something went wrong'
            print(f'Error while stopping freedom-0{server}: {e}')
            await ctx.send(embed=em)
        else:
            await tempm.delete()
            if 'error' in attempt.lower():
                em.title = 'Command error'
                em.colour = 0xFF0000
                em.description = f'freedom-0{server}: {attempt}'
                await ctx.send(embed=em)
            else:
                em.title = 'Success'
                em.colour = 0x00FF00
                em.description = f'freedom-0{server}: {attempt}'
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
            if args[0] in ['mute', 'stfu', 'gtfo', 'ban', 'unban', 'unmute', 'smite', 'noob', 'tban', 'tempban', 'warn',
                           'mv', 'kick', 'cc', 'say', 'autoclear', 'autotp', 'toggle']:
                self.write_telnet_session(server,
                                          bytes(command, 'ascii') + b"\r\n")
            elif args[0] == 'saconfig':
                if args[1] not in ['add', 'remove']:
                    raise NoPermission(['SACONFIG_EDIT_FROM_ADMIN_CONSOLE'])
                else:
                    self.write_telnet_session(server,
                                              bytes(command, 'ascii') + b"\r\n")
            else:
                raise notAdminCommand()
        except Exception as e:
            em.title = 'Command error'
            em.colour = 0xFF0000
            em.description = f'{e}'
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = f'Command sent to freedom-0{server}.'
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
                em.description = f'freedom-0{server}: {attempt}'
                await ctx.send(embed=em)
            else:
                em.title = 'Success'
                em.colour = 0x00FF00
                em.description = f'freedom-0{server}: {attempt}'
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
            print(f'Error while restarting freedom-0{server}: {e}')
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = f'freedom-0{server} restarting.'
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
            em.description = f'Command sent to freedom-0{server}.'
            await ctx.send(embed=em)

    @commands.command(aliases=['status'])
    async def state(self, ctx):
        """Gets the current status of the Server."""
        em = discord.Embed()
        server = 1
        if ctx.channel.id == 793632795598913546:
            server = 2
        if get_server_status(server):
            em.description = f'freedom-0{server} is online'
            em.colour = 0x00FF00
        else:
            em.description = f'freedom-0{server} is offline'
            em.colour = 0xFF0000
        await ctx.send(embed=em)

    @commands.command(name='list', aliases=['l', 'who', 'lsit'])
    async def online(self, ctx):
        """Gives a list of online players."""
        if ctx.channel.id == self.bot.gmod_server_chat:
            return
        em = discord.Embed()
        config_file = read_json('config')
        if ctx.channel.id == 793632795598913546:
            ip = config_file['SERVER_IP_2']
            server = 2
        else:
            ip = config_file['SERVER_IP']
            server = 1
        port = config_file['PLAYERLIST_PORT']
        em.title = f"Player List - freedom-0{server}"
        try:
            json = requests.get(f"http://{ip}:{port}/list?json=true", timeout=5).json()
            if json["online"] == 0:
                em.description = "There are no online players"
            else:
                ranks = list(json.keys())

                entries = []

                for rank in ranks:
                    if rank not in ['max', 'online'] and json[rank]:
                        rank_fixed = rank.split('_')
                        for word in range(len(rank_fixed)):
                            rank_fixed[word] = rank_fixed[word].capitalize()
                        entries.append(format_list_entry(em, json[rank], f'{" ".join(rank_fixed)}'))

                order = ['Owners', 'Executives', 'Developers', 'Senior Admins', 'Admins', 'Master Builders',
                         'Operators', 'Imposters']

                players = {}
                rank_categories = ["owners", "master_builders", "senior_admins", "imposters", "executives",
                                   "developers", "operators", "admins"]
                for x in json:
                    if x in rank_categories:
                        players[x] = json[x]
                print(players)
                em.description = f"There are {get_visible_player_count(players)} / {json['max']} online players"
                sorted_ranks = [entry for rank in order for entry in entries if entry.name == rank]

                for x in sorted_ranks:
                    em.add_field(name=f'{x.name} ({x.playercount})', value=x.value, inline=False)

        except Exception as e:
            em.description = 'Server is offline'
            print(e)
        await ctx.send(embed=em)

    @commands.command()
    async def ip(self, ctx):
        """Returns the server IP."""
        await ctx.send(embed=discord.Embed(description='play.totalfreedom.me', title='Server IP'))

    @commands.command()
    @is_staff()
    async def archivereports(self, ctx):
        """Archive all in-game reports older than 24 hours."""
        count = 0
        reports_channel = self.bot.get_channel(self.bot.reports_channel_id)
        archived_reports_channel = self.bot.get_channel(
            self.bot.archived_reports_channel_id)
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

            print(
                f'TPS: {server_tps} UPTIME: {server_uptime} MAX MEM: {maximum_memory} ALLCTD MEM: {allocated_memory} FREE MEM: {free_memory}')

            try:
                server_uptime = \
                    re.match('([0-9]+ days? )?([0-9]+ hours )?([0-9]+ minutes )?([0-6]?[0-9] seconds)', server_uptime)[
                        0]
                server_tps = re.match('[0-2][0-9].?[0-9]*', server_tps)[0]
                maximum_memory = re.match('[0-9]+,?[0-9]* MB', maximum_memory)[0]
                allocated_memory = re.match('[0-9]+,?[0-9]* MB', allocated_memory)[0]
                free_memory = re.match('[0-9]+,?[0-9]* MB', free_memory)[0]
            except Exception as e:
                em.description = f'Something went wrong: {e}'
                em.colour = 0xFF0000
            else:
                em.add_field(name='TPS', value=server_tps, inline=False)
                em.add_field(name='Uptime', value=server_uptime, inline=False)
                em.add_field(name='Maximum Memory', value=maximum_memory, inline=False)
                em.add_field(name='Allocated Memory', value=allocated_memory, inline=False)
                em.add_field(name='Free Memory', value=free_memory, inline=False)
        else:
            em.description = 'Server is offline'
        await ctx.send(embed=em)

    @commands.command()
    @is_mod_or_has_perms()
    async def fixreports(self, ctx):
        await ctx.channel.trigger_typing()
        reports_channel = self.bot.get_channel(self.bot.reports_channel_id)
        messages = await reports_channel.history(limit=500).flatten()
        fixed = 0
        for message in messages:
            if len(message.reactions) == 0 and message.author == message.guild.me:
                await message.add_reaction(clipboard)
                fixed += 1
        await ctx.send(f'Fixed **{fixed}** reports')

    @commands.command(aliases=['selfrestart', 'ar'], usage='tf!autorestart [on|off]')
    @is_dev()
    async def autorestart(self, ctx, *opt):
        """Toggle the auto-restart feature.     Usage: tf!autorestart [on|off]"""
        em = discord.Embed()
        em.title = 'Automatic restart'
        if not opt:
            self.bot.auto_restart = not self.bot.auto_restart
        elif opt[0].lower() in ['on', 'true']:
            self.bot.auto_restart = True
        elif opt[0].lower() in ['off', 'false']:
            self.bot.auto_restart = False
        else:
            em.description = 'Invalid arguements'
            em.colour = 0xFF0000
            await ctx.send(embed=em)
            return
        if self.bot.auto_restart:
            em.description = 'Servers will now automatically restart'
            em.colour = 0x00FF00
        if not self.bot.auto_restart:
            em.description = 'Servers will no longer automatically restart'
            em.colour = 0xFF0000

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(ServerCommands(bot))
