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

########## Class ##########

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

########## Events ##########

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="br!help"))
        print("bot is ready")



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, delete_after=5):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"``{error}!``", delete_after=120)
            await ctx.message.delete()



        @tasks.loop(seconds=5)
        async def change_status(self):
            await self.change_presence(activity=discord.Game(next(self.status)))

########## Setup ##########

def setup (client):
    client.add_cog(Events(client))