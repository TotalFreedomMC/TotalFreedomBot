import discord

from discord.ext import commands

server_liaison = 769659653096472634
event_host = 769659653096472629
server_banned = 769659653096472636
senior_admin = 769659653129896016
admin = 769659653121900553
master_builder = 769659653121900550
reports_channel_id = 769659654791233585
archived_reports_channel_id = 769659655033978900
guild_id = 769659653096472627
mentions_channel_id = 769659654027739151
discord_admin = 769659653129896025
discord_mod = 769659653129896023
devs = [114348811995840515, 147765181903011840]
bot_logs_channel_id = 771391406609662013
executive = 769659653129896019
asst_exec = 769659653129896018
developer = 769659653129896017
creative_designer = 771748500576141332
master_builder = 769659653121900550

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

def is_dev():
    def predicate(ctx):
        user = ctx.message.author
        if user.id in devs:
            return True
        else:
            raise no_permission(['BOT_DEVELOPER'])
    return commands.check(predicate)

def is_mod_or_has_perms(**permissions):
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id in [discord_mod, discord_admin] or permissions:
                return True
        else:
            raise no_permission(['IS_MOD_OR_HAS_PERMS'])
    return commands.check(predicate)

def is_executive():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id in [executive, asst_exec]:
                return True
        else:
            raise no_permission(['IS_EXECUTIVE'])
    return commands.check(predicate)

    
def is_tf_developer():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == developer:
                return True
        else:
            raise no_permission(['IS_TOTALFREEDOM_DEVELOPER'])
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

def is_creative_designer():
    def predicate(ctx):
        user = ctx.message.author
        for role in user.roles:
            if role.id == creative_designer:
              return True
        else:
            raise no_permission(['IS_CREATIVE_DESIGNER'])  
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
