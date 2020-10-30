import discord
import time

from telnetlib import Telnet
from discord.ext import commands

class telnet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ip = [ip]
        self.telnet_port = [port]
        self.telnet_password = [password]
    
        self.bot.telnet_session = Telnet(self.ip, self.telnet_port)
        self.read_timeout = 3
        if b'Username:' in self.bot.telnet_session.read_until(b'Username:', timeout=self.read_timeout):
            self.bot.telnet_session.write(bytes('TotalFreedom', 'ascii') + b"\r\n")
            
            if b'Password:' in self.bot.telnet_session.read_until(b'Password:', timeout=self.read_timeout):
                time.sleep(2)
                self.bot.telnet_session.write(bytes(self.telnet_password, 'ascii') + b"\r\n")
        else:
            raise PyboardError('Failed to establish a telnet connection with the board')
    
    def connect():
        self.bot.telnet_session = Telnet(self.ip, self.telnet_port)
        self.read_timeout = 3
        if b'Username:' in self.bot.telnet_session.read_until(b'Username:', timeout=self.read_timeout):
            self.bot.telnet_session.write(bytes('TotalFreedom', 'ascii') + b"\r\n")
            
            if b'Password:' in self.bot.telnet_session.read_until(b'Password:', timeout=self.read_timeout):
                time.sleep(2)
                self.bot.telnet_session.write(bytes(self.telnet_password, 'ascii') + b"\r\n")
        else:
            raise PyboardError('Failed to establish a telnet connection with the board')
        
def setup(bot):
    bot.add_cog(telnet(bot))
