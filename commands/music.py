import discord
import datetime
import lavalink
import os

from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx):
        vc = ctx.author.voice.channel
        voiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voiceClient and voiceClient.is_connected():
            await voiceClient.move_to(vc)
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] The bot has moved to {vc} in {ctx.guild.name}\n")
            await ctx.send(f'Joined `{vc.name}`')
        else:
            await vc.connect()
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] The bot has connected to {vc} in {ctx.guild.name}\n")
            await ctx.send(f'Joined `{vc.name}`')
    
    @commands.command()
    async def leave(self, ctx):
        vc = ctx.author.voice.channel
        voiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        if voiceClient and voiceClient.is_connected():
            await voiceClient.disconnect()
            await ctx.send(f'Left `{vc.name}`')
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] The bot has disconnected from {vc.name} in {ctx.guild.name}\n")
        else:
            await ctx.send(f"{ctx.author.name.mention} you fat retard i'm not connected to a vc")
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] {ctx.author} failed running: {ctx.message.content} in guild: {ctx.guild.name}')
    # Not Working
    @commands.command(aliases=['p', 'pla'])
    async def play(self, ctx, url):
        em = discord.Embed
        em.title = 'Music'
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            em.description = 'Music is currently being played.'
            em.colour = 0xFF0000
            await ctx.send(embed=em)
            return
    
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
    
        
    
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")
    
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
    
    
        nname = name.rsplit("-", 2)
        em.description = f"Playing: {nname[0]}"
        em.colour = 0x00FF00
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Music(bot))
