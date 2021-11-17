########## Imports ##########

import discord
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
import aiohttp
import asyncpraw

########## Class ##########

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

########## Commands ##########

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *, member : discord.Member = None):
        if not member:
            member = ctx.message.author

        member = ctx.author if not member else member
        em = discord.Embed(
            title = f'**Avatar Command**',
            color = 0xD71E8C,
            description = f"Showing Avatar of **{member.name}**!",
            timestamp = ctx.message.created_at

        )

        em.set_image(url = member.avatar_url)
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()



    @commands.command(aliases = ['8ball'])
    @commands.guild_only()
    async def _8ball(self, ctx, *, question):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]


        em = discord.Embed(
            title = '**8ball Command**',
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at
        )

        em.add_field(name = (f'You Questioned: {question}'), value = (f'The response is: {random.choice(responses)}'))
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect arguments! Please say a question to answear!", delete_after=120)
            await ctx.message.delete()



    @commands.command(aliases = ['F'])
    @commands.guild_only()
    async def f(self, ctx):

        em = discord.Embed(
            title = "**F in Chat Command**",
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        em.set_image(url = "https://media1.tenor.com/images/ae2c3dbeb7ccf68ea749b9ba7abe1919/tenor.gif")
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @commands.command(aliases = ['howgae'])
    @commands.guild_only()
    async def howgay(self, ctx, member : discord.Member):
    
        responses = [ 
        random.randint(0,100)
        ]

        em = discord.Embed(
            title = "**How Gay Command**",
            color = 0xD71E8C,
            description = f"@{member.name} is: {random.choice(responses)}% gay!",
            timestamp = ctx.message.created_at

        )
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @howgay.error
    async def howgay_error(self, ctx, error):
         if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect arguments! Please mention somebody who you want to see how gay is it.")
            await ctx.message.delete()

    @commands.command(aliases = ['rolldice'])
    @commands.guild_only()
    async def dice(self, ctx):
        tyt = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6"
        ]


        em = discord.Embed(
            title = '**RollDice Command**',
            color = 0xD71E8C,
            description = f"**You rolled: {random.choice(tyt)}**",
            timestamp = ctx.message.created_at
        )

        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @commands.command(aliases = ['OOF'])
    @commands.guild_only()
    async def oof(self, ctx):

        em = discord.Embed(
            title = "**OOF Command**",
            color = 0xD71E8C,
            description = "",
            timestamp = ctx.message.created_at

        )
        em.set_image(url = "https://media1.tenor.com/images/5070d308bf892e7fdd36a1db83d861ec/tenor.gif")
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @commands.command(aliases = ['meme'])
    @commands.guild_only()
    async def memes(self, ctx):
 
        emb = discord.Embed(
            title = "**Meme Command**",
            color = 0xD71E8C,
            description = f"Meme generating...",
            timestamp = ctx.message.created_at

        )
        emb.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ctx.send(embed = emb, delete_after=5)

        reddit = asyncpraw.Reddit(
            client_id = "tf3Ul0NFp0C6zKI1jMy2hA",
            client_secret = "CwprifAVWQRWdcbevv3Hpa3M1xDwQg",
            username = "Ender_the_Player",
            password = "4Jtng0$4xLQV",
            user_agent="anything"
        )

        subreddit =  await reddit.subreddit("memes")
        top = subreddit.top(limit = 50)
        all_subs = []

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url

        em = discord.Embed(
            title = "**Meme Command**",
            color = 0xD71E8C,
            description = f"{name}",
            timestamp = ctx.message.created_at

        )
        em.set_image(url = url)
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)



        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

########## Setup ##########

def setup (client):
    client.add_cog(Fun(client))