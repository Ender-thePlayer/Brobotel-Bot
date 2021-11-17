########## Import ##########

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

class User(commands.Cog):

    def __init__(self, client):
        self.client = client

########## Commands ##########

    """@commands.command()
    @commands.guild_only()
    async def test(self, ctx():
        member = ctx.author if not member else member
        em = discord.Embed(
            title = "Here are the Bot's info:",
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        em.add_field(name = "Build:", value = "BETA-13621_008-1", inline = False)
        em.add_field(name = "Status:", value = "Online", inline = False)
        em.add_field(name = "Is in:", value = f"{str(len(client.guilds))} servers")

        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()"""


    @commands.command()
    @commands.guild_only()
    async def info(self, ctx, *, member : discord.Member = None):
        member = ctx.author if not member else member
        em = discord.Embed(
            title = "**Bot Info Command**",
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        em.add_field(name = "Build:", value = "pre-1.6_0058", inline = False)
        em.add_field(name = "Is in:", value = f"{str(len(self.client.guilds))} servers", inline = False)
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx, *, member : discord.Member = None):
        member = ctx.author if not member else member

        em = discord.Embed(
            title = "**Ping Command**",
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        em.add_field(name = "Ping:", value = f"{round(self.client.latency * 1000)}ms", inline = False)
        em.add_field(name = "Server:", value = "heroku-eu", inline = False)

        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @commands.command(aliases = ['help'])
    @commands.guild_only()
    async def _help(self, ctx, arg = None):

        em = discord.Embed(
            title = "**Help Command**",
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        em.add_field(name= "Use br!help mod:",  value = "To see help for moderation commands!")
        em.add_field(name= "Use br!help user:",  value =  "To see all the bot's user commands!")
        em.add_field(name= "Use br!help fun:",  value =  "To see all the fun commands!")
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)


        emed = discord.Embed(
            title = "**Help Command**",
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        emed.add_field(name = "We sended help in your DM!", value = "You need to allow DM messages from server members for the help to show!", inline=False)
        emed.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)


        embed = discord.Embed(
            title = '**Mod Commands**',
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at
 
    )
        embed.add_field(name = "| br!clear {nr}", value = "Clears {nr} of messages! The default is 10!", inline=False)
        embed.add_field(name = "| br!new", value = "Creates a new ticket!", inline=False)
        embed.add_field(name = "| br!close", value = "Closes a specific ticket!", inline=False)
        embed.add_field(name = "| br!kick {member}", value = "Kicks {member} from your server!", inline=False)
        embed.add_field(name = "| br!ban {member}", value = "Bans {member} from your server!", inline=False)
        embed.add_field(name = "| br!unban {username}", value = "Unbans {username} from your server! (Ex: br!unban Ender#4783)", inline=False)
        embed.add_field(name = "| br!userinfo {username}", value = "Shows the user's info!", inline=False)
        embed.add_field(name = "| br!serverinfo", value = "Shows the respective server`s info!", inline=False)
        embed.add_field(name = "| br!slowmode {seconds}", value = "Set a slowmode or disable by not specifying {seconds}!", inline=False)

        embed.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        emb = discord.Embed(
            title = '**User Commands**',
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        emb.add_field(name = "| br!changelogs", value = "Shows the bot's newest big update! (more updates are on the website)", inline=False)
        emb.add_field(name = "| br!info", value = "Shows the bot's build name and how many servers is in!", inline=False)
        emb.add_field(name = "| br!ping", value = "Shows the bot's ping and server location!", inline=False)
        emb.add_field(name = "| br!help", value = "Shows all the bot's commands!", inline=False)
        emb.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        embd = discord.Embed(
            title = '**Fun Commands**',
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at
 
            )
        embd.add_field(name = "| br!avatar {mention}", value = "Shows {mention}'s avatar! If you not specify {mention} it will show your avatar!", inline=False)
        embd.add_field(name = "| br!8ball {question}", value = "8ball command!", inline=False)
        embd.add_field(name = "| br!howgay {mention}", value = "Shows how gay is {mention}!", inline=False)
        embd.add_field(name = "| br!f", value = "Press F in Chat!", inline=False)
        embd.add_field(name = "| br!oof", value = "Say OOF!", inline=False)
        embd.add_field(name = "| br!dice", value = "Roll a dice!", inline=False)
        embd.add_field(name = "| br!meme", value = "Shows a meme!", inline=False)
        embd.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        if arg == None:
            await ctx.send(embed = em)
            await ctx.message.delete()
        elif arg == "mod":
            await ctx.author.send(embed = embed)
            await ctx.send(embed = emed, delete_after=120)
            await ctx.message.delete()
        elif arg == "user": 
            await ctx.author.send(embed = emb)
            await ctx.send(embed = emed, delete_after=120)
            await ctx.message.delete()
        elif arg == "fun":
            await ctx.author.send(embed = embd)
            await ctx.send(embed = emed, delete_after=120)
            await ctx.message.delete()


    @commands.command(aliases = ['changelog'])
    @commands.guild_only()
    async def changelogs(self, ctx):

        em = discord.Embed(
            title = "**Changelogs Command**",
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)
        em.add_field(name= "Changelogs Command is Unavable!",  value = "We're sorry but this command is unavable at this moment!")

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()
 
########## Setup ##########

def setup (client):
    client.add_cog(User(client))
