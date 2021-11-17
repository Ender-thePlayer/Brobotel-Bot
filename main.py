########## Imports ##########

import discord
from discord.ext.commands.errors import MissingPermissions, CheckFailure
from discord.ext import commands,tasks
from operator import mod
from discord.embeds import Embed
from itertools import cycle
import random 
import asyncio
import os
from os import listdir
from os.path import realpath, split, join, splitext
import json

########## Client ##########

intents= discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = ['br!','Br!'])
client.remove_command('help')

########## Cogs ##########

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

########## Token ##########

client.run("ODA0NzYxNTU4MjI3MzUzNjAx.YBRCmw.n1Zqv9ICKzCDO2xXMJ2asAE5m14")