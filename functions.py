import discord
import json
import requests

from discord.ext import commands
from checks import *

def format_list_entry(embed, list, name):
    embed.add_field(name="{} ({})".format(name, len(list)), value=", ".join(list), inline=False)
    return embed
  
def did_mention_other_user(users, author):
    for user in users:
        if user is not author:
            return True
    return False

def removed_user_mentions(old, new):
    users = []
    for user in old:
        if user not in new:
            users.append(user)
    return users

def removed_role_mentions(old, new):
    roles = []
    for role in old:
        if role not in new:
            roles.append(role)
    return roles

def get_avatar(user, animate=True):
    if user.avatar_url:
        avatar = str(user.avatar_url).replace(".webp", ".png")
    else:
        avatar = str(user.default_avatar_url)
    if not animate:
        avatar = avatar.replace(".gif", ".png")
    return avatar

def read_json(file_name):
    with open(f'/root/totalfreedom/{file_name}.json', 'r') as file:
        data = json.load(file)
    return data

def write_json(file_name, data):
    with open(f'/root/totalfreedom/{file_name}.json', 'w') as file:
        json.dump(data,file,indent=4)
    return data

def hit_endpoint(command):
    url = [CENSORED_URL]
    payload = {}
    headers = {}

    response = json.loads(requests.request("GET", url, headers=headers, data = payload, timeout=100).text)
    return response['response']
