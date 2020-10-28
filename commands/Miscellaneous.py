import discord
import asyncio

from discord.ext import commands
from checks import *

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @is_dev()
    @commands.command(pass_context=True)
    async def killbot(self, ctx):
        em = discord.Embed()
        em.description = 'Bot offline.'
        await ctx.send(embed=em)
        await self.bot.logout()
  
    @is_dev()
    @commands.command(name='debug')
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