import discord
import asyncio
import telnet
import time
import events
import os

from datetime import datetime
from discord.ext import commands
from checks import *
from functions import *

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @is_dev()
    @commands.command()
    async def killbot(self, ctx):
        em = discord.Embed()
        em.description = 'Bot offline.'
        await ctx.send(embed=em)
        await self.bot.logout()
        return
    
    @is_tf_developer()
    @commands.command()
    async def telnetconfig(self, ctx, *args):
        em = discord.Embed()
        em.title = 'Telnet config'
        if not args or args[0] in ['reconnect', 'connect']:
            try:
                self.bot.telnet_object.connect()
            except Exception as e:
                em.description = f'Failed reconnection: {e}'
                em.colour = 0xFF0000
            else:
                em.description = 'Reconnection successful'
                em.colour = 0x00FF00
        elif args[0] == 'name':
            try:
                self.bot.telnet_object.session.close()
                self.bot.telnet_object.connect(args[1])
                events.telnet_username = self.bot.telnet_object.username
                config = read_json('config')
                config['TELNET_USERNAME'] = self.bot.telnet_object.username
                write_json('config', config)
            except Exception as e:
                em.description = f'Failed config edit: {e}'
                em.colour = 0xFF0000
            else:
                em.description = 'Configuration successful'
                em.colour = 0x00FF00
            
        elif args[0] == 'test':
            command = ''
            for x in range(1, len(args)):
                command += f'{args[x]} '
            time_sent = str(datetime.utcnow().replace(microsecond=0))[11:]
            
            self.bot.telnet_object.session.write(bytes(command, 'ascii') + b"\r\n")
            self.bot.telnet_object.session.read_until(bytes(f'{time_sent} INFO]:', 'ascii'), 2)
            if ctx.channel == ctx.guild.get_channel(server_chat):
                self.bot.telnet_object.session.read_until(bytes('\r\n', 'ascii'), 2)
            next_line = self.bot.telnet_object.session.read_until(bytes('\r\n', 'ascii'), 2)
            em.description = f"Response from server: {next_line.decode('utf-8')}"
        else:
            em.description = f'Command **{args[0]}** not found.'
            em.colour = 0xFF0000
        
        await ctx.send(embed=em)
    
    @is_dev()
    @commands.command()
    async def debug(self, ctx, *, cmd):
        'Executes a line of code'
        try:
            result = eval(cmd)
            if asyncio.iscoroutine(result):
                result = await result
            await ctx.send(f'''```py
{result}```''')
        except Exception as e:
            await ctx.send(f'''```py
{type(e).__name__}: {e}```''')

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
