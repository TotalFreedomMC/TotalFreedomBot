import json
import requests
import os
import itertools

from discord.ext import commands
from checks import *

class embed_entry:
    def __init__(self, name, value, *, playercount):
        self.name = name
        self.value = value
        if playercount:
            self.playercount = playercount
        
def format_list_entry(embed, l, name):
    l_names = [f'{l[i]}' for i in range(len(l))]
    l_names = [name.replace('_', '\_') for name in l_names]
    
    em = embed_entry(
            name=name,
            value=", ".join(l_names),
            playercount = len(l)
        )
    return em


def get_prefix(client, message):
    #prefixes = ['TF!', 'Tf!', 'tF!', 'tf!']
    prefix = os.getenv('prefix')
    prefixes = map(''.join, itertools.product(*((letter.upper(), letter.lower()) for letter in prefix)))
    return commands.when_mentioned_or(*prefixes)(client, message)


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
        json.dump(data, file, indent=4)
    return data


def hit_endpoint(command, server=1):
    config_file = read_json('config')
    if server == 1:
        ip = config_file['SERVER_IP']
        pw = config_file['ENDPOINTS_PW']
    else:
        ip = config_file['SERVER_IP_2']
        pw = config_file['ENDPOINTS_PW_2']
    port = config_file['ENDPOINTS_PORT']
    url = f"http://{ip}:{port}?password={pw}&command={command}"
    payload = {}
    headers = {}
    try:
        response = json.loads(requests.request(
            "GET", url, headers=headers, data=payload, timeout=5).text)
    except:
        response = {'response': 'Connection Error.'}
    return response['response']
    
def get_server_status(server=1):
    config_file = read_json('config')
    if server == 1:
        ip = config_file['SERVER_IP']
    else:
        ip = config_file['SERVER_IP_2']
    port = config_file['PLAYERLIST_PORT']
    try:
        requests.get(f"http://{ip}:{port}/list?json=true", timeout=5).json()
    except:
        return False
    else:
        return True
