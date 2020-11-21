import discord
import datetime

from discord.ext import commands
from checks import *
from functions import *

muted_role_id = 769659653121900546

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moderator_role_id = 769659653129896023
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason specified"):
        """Kicks a user from the guild."""
        await user.kick(reason=f'{reason}**  **by: {ctx.author.name}')
        await ctx.send(embed=discord.Embed(embed=f'{user.name} has been kicked by: {ctx.author.name} for reason: {reason}'))
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Kicked {user.name} from {ctx.guild.name}")

    @commands.command(aliases=['gtfo'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason specified"):
        """Bans a user from the guild."""
        await user.ban(reason=f'{reason} || by: {ctx.author.name}', delete_message_days=0)
        await ctx.send(embed=discord.Embed(description=f'{user.name} has been banned by: {ctx.author.name} for reason: {reason}'))
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Banned {user.name} from {ctx.guild.name}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason="No reason specified"):
        """Unbans a user from the guild."""
        await ctx.guild.unban(user, reason=f'{reason} || by: {ctx.author.name}')
        await ctx.send(embed=discord.Embed(description=f'{user.name} has been unbanned by: {ctx.author.name} for reason: {reason}'))
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Banned {user.name} from {ctx.guild.name}")

    @commands.command(aliases=['massdelete','purge'])
    @commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, msgs):
        """Purge messages from a channel."""
        channel = ctx.channel
        await channel.purge(limit=(int(msgs) + 1))
        await ctx.send(embed=discord.Embed(description=f'{ctx.author.name} deleted {msgs} messages'))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] {ctx.author.name} purged {msgs} messages in {ctx.guild.name}')

    @commands.command(aliases=['stfu'])
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=''):
        """Mutes a member of the server."""
        muted_role = ctx.guild.get_role(muted_role_id)
        await member.add_roles(muted_role, reason = f'{reason} || by {ctx.author.name}')
        if reason == '':
            reason = 'No reason specified'
        await ctx.send(embed=discord.Embed(description=f'{member} muted by: {ctx.author.name} for: {reason}'))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Muted {member} in {ctx.guild.name}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=''):
        """Unmutes a member of the server."""
        muted_role = ctx.guild.get_role(muted_role_id)
        await member.remove_roles(muted_role, reason = f'{reason} || by {ctx.author.name}')
        await ctx.send(embed=discord.Embed(description=f'{member} unmuted by {ctx.author.name}'))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Unmuted {member} in {ctx.guild.name}')
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setreaction(self, ctx, role : discord.Role=None, msg : discord.Message=None, emoji=None):
        if role and msg and emoji :
            await msg.add_reaction(emoji)
            self.bot.reaction_roles.append([role.id,msg.id,emoji])
            data = read_json('config')
            data['reaction_roles'].append([role.id,msg.id,emoji])
            print(data['reaction_roles'])
            write_json('config', data)
    
def setup(bot):
    bot.add_cog(Moderation(bot))
