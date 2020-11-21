import discord
import random
import aiofiles
import time
import checks
import logscript

from datetime import datetime
from discord.ext import commands
from checks import *
from functions import *
from unicode import *
from telnet import telnet

telnet_ip = "localhost"
telnet_port = 22
telnet_username = "root"
telnet_password = "root"
print = logscript.logging.getLogger().critical

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        config = read_json('config')
        telnet_ip = config['TELNET_IP']
        telnet_port = config['TELNET_PORT']
        telnet_username = config['TELNET_USERNAME']
        telnet_password = config['TELNET_PASSWORD']
        
        self.bot.reaction_roles = []
        self.bot.telnet_object = telnet(telnet_ip, telnet_port, telnet_username, telnet_password)
        self.bot.telnet_object.connect()
        
        print(f'[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [TELNET] Bot logged into Telnet as: {self.bot.telnet_object.username}')
        
        reaction_data = read_json('config')
        self.bot.reaction_roles = reaction_data['reaction_roles']
        
        print(f'[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Client] {self.bot.user.name} is online.')
        game = discord.Game('play.totalfreedom.me')
        await self.bot.change_presence(status=discord.Status.online, activity=game)
    
        guildCount = len(self.bot.guilds)
        print(f'[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Guilds] bot currently in {guildCount} guilds.')
        for guild in self.bot.guilds:
            print(f'[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Guilds] Connected to guild: {guild.name}, Owner: {guild.owner}')
        global starttime
        starttime = datetime.utcnow()
        
    
    '''@commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and message.author is message.guild.me and message.channel.id == reports_channel_id:
            await message.add_reaction(clipboard)
        if message.type == discord.MessageType.new_member:
            if re.search('discord\.gg\/[a-zA-z0-9\-]{1,16}', message.author.name.lower()) or re.search('discordapp\.com\/invite\/[a-z0-9]+/ig', message.author.name.lower()):
                await message.author.ban(reason="Name is an invite link.")
                await message.delete()
        bypass_roles = [discord_admin, discord_mod]
        bypass = False
        if message.author != self.bot.user:
            for role in message.author.roles:
                if role.id in bypass_roles:
                    bypass = True
        else:
            if 'Server has started' in message.content: # Telnet reconnect script
                try:
                    self.bot.telnet_object.connect()
                except Exception as e:
                    print(f'Failed to reconnect telnet: {e}')
                    time.sleep(5)
                    try:
                        self.bot.telnet_object.connect()
                    except Exception as fuckup:
                        print(f'Second attempt failed to reconnect telnet: {fuckup}')

        if not bypass:
            if re.search('discord\.gg\/[a-zA-z0-9\-]{1,16}', message.content) or re.search('discordapp\.com\/invite\/[a-z0-9]+/ig', message.content):
                await message.delete()
                await message.channel.send(f"{message.author.mention} do not post invite links to other discord servers.")
                return'''
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not isinstance(before.author, discord.Member):
            return
        if before.guild.id != guild_id:
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
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
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
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        em = discord.Embed()
        em.title = 'Command Error'
        em.description = f'{error}'
        em.colour = 0xFF0000
        await ctx.send(embed=em)
        print(f'[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Commands] {ctx.author} (ID: {ctx.author.id}) failed running: {ctx.message.content} in guild: {ctx.guild.name}')
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(f'[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: [Commands] {ctx.author} (ID: {ctx.author.id}) ran: {ctx.message.content} in guild: {ctx.guild.name}')
        bot_logs_channel = self.bot.get_channel(bot_logs_channel_id)
        log = discord.Embed(title='Logging', description=f'{ctx.author} (ID: {ctx.author.id}) ran: {ctx.message.content}', colour=0xA84300)
        await bot_logs_channel.send(embed=log)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member == self.bot.user:
            pass
        else:
            for role_id, msg_id, emoji in self.bot.reaction_roles:
                if msg_id == payload.message_id and emoji == str(payload.emoji.name):
                    await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(role_id), reason='reaction')
            if payload.channel_id == reports_channel_id:
                guild = self.bot.get_guild(guild_id)
                reports_channel = self.bot.get_channel(reports_channel_id)
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
                        archived_reports_channel = self.bot.get_channel(archived_reports_channel_id)
                        await report.delete()
                        await archived_reports_channel.send("Handled by " + guild.get_member(payload.user_id).mention, embed=embed)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.member == self.bot.user:
            pass
        else:
            for role_id, msg_id, emoji in self.bot.reaction_roles:
                if msg_id == payload.message_id and emoji == str(payload.emoji.name):
                    await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(self.bot.get_guild(payload.guild_id).get_role(role_id), reason='reaction')
                    
def setup(bot):
    bot.add_cog(Events(bot))
