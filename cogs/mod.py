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

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

########## Commands ##########

    @commands.command(aliases= ['purge','delete'])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(self, ctx, amount: int=None): # Set default value as None
        if amount == None:
            await ctx.channel.purge(limit=11)
            await ctx.send("Cleared 10 messages!", delete_after=120)

        else:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Cleared {amount} messages!", delete_after=120)


    @clear.error
    async def clear_error(self, ctx, error):

        if isinstance(error, CheckFailure):
            await ctx.send('You don`t have the permission to use this command!', delete_after=120)
            await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member : discord.Member,*, reason = None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention} with reason: ``{reason}``", delete_after=120)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect arguments! Please mention the user you want to kick and optionally a reason!", delete_after=120)
            await ctx.message.delete()
        else:
            if isinstance(error, CheckFailure):
                await ctx.send('You don`t have the permission to use this command!', delete_after=120)
                await ctx.message.delete()
             
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member : discord.Member,*, reason = None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} with reason: ``{reason}``", delete_after=120)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect arguments! Please mention the user you want to ban and optionally a reason!", delete_after=120)
            await ctx.message.delete()
        else:
            if isinstance(error, CheckFailure):
                await ctx.send('You don`t have the permission to use this command!', delete_after=120)
                await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, *, member):
        banned_users= await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}", delete_after=120)
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect arguments! Please type the name of the user you want to ban! (Ex. ``br!unban Ender#4783``", delete_after=120)
            await ctx.message.delete()
        else:
         if isinstance(error, CheckFailure):
            await ctx.send('You don`t have the permission to use this command!', delete_after=120)
            await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def new(self, ctx, *, args = None):

        await self.client.wait_until_ready()

        if args == None:
            message_content = "Please wait, we will be with you shortly!"
    
        else:
            message_content = "".join(args)

        with open("data.json") as f:
            data = json.load(f)

        ticket_number = int(data["ticket-counter"])
        ticket_number += 1

        ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

        for role_id in data["valid-roles"]:
            role = ctx.guild.get_role(role_id)

            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

        em = discord.Embed(
            title = "**New Ticket Command**",
            color = 0xD71E8C,
            description = f"New Ticket Made by {ctx.author.name}#{ctx.author.discriminator}",
            timestamp = ctx.message.created_at

        )
        em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

        await ticket_channel.send(embed=em)

        pinged_msg_content = ""
        non_mentionable_roles = []

        if data["pinged-roles"] != []:

            for role_id in data["pinged-roles"]:
                role = ctx.guild.get_role(role_id)

                pinged_msg_content += role.mention
                pinged_msg_content += " "
    
                if role.mentionable:
                    pass
                else:
                    await role.edit(mentionable=True)
                    non_mentionable_roles.append(role)
        
            await ticket_channel.send(pinged_msg_content)

            for role in non_mentionable_roles:
                await role.edit(mentionable=False)
    
        data["ticket-channel-ids"].append(ticket_channel.id)

        data["ticket-counter"] = int(ticket_number)
        with open("data.json", 'w') as f:
            json.dump(data, f)
    
    
        created_em = discord.Embed(
            title = '**New Ticket Command**',
            color = 0xD71E8C,
            description = f"A new ticket Has Appeared at {ticket_channel.mention}!",
            timestamp = ctx.message.created_at

        )
        created_em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)
    
        await ctx.send(embed=created_em, delete_after=120)
        await ctx.message.delete()



    @commands.command()
    @commands.guild_only()
    async def close(self, ctx):
        with open('data.json') as f:
            data = json.load(f)
    
        if ctx.channel.id in data["ticket-channel-ids"]:

            channel_id = ctx.channel.id

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

            try:

                em = discord.Embed(
                    title = '**Close Ticket Command**',
                    color = 0xD71E8C,
                    description = "Are you sure you want to close this ticket? Reply with `close` if you are sure.",
                    timestamp = ctx.message.created_at
               )
                em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)
         

                await ctx.send(embed=em, delete_after=60)
                await ctx.message.delete()
                await self.client.wait_for('message', check=check, timeout=60)
                await ctx.channel.delete()
            

                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]

                with open('data.json', 'w') as f:
                    json.dump(data, f)
        
            except asyncio.TimeoutError:
                em = discord.Embed(
                    title = '**Time Error**',
                    color = 0xD71E8C,
                    description = "You have run out of time to close this ticket. Please run the command again.",
                    timestamp = ctx.message.created_at
                )
                em.set_footer(text = f'Invoked by: @{ctx.author}!', icon_url = ctx.author.avatar_url)

                await ctx.send(embed=em, delete_after=120)
                await ctx.message.delete()



    @commands.command()
    @commands.guild_only()
    async def userinfo(self, ctx, *, member : discord.Member = None):

        if not member:
            member = ctx.message.author

        roles = [role for role in member.roles]

        em = discord.Embed(
        
            title = f"**UserInfo Command**",
            description = f"",
            color = 0xD71E8C
        )

        em.set_thumbnail(url = member.avatar_url)
        em.set_footer(text = f"Invoked by: {ctx.author}", icon_url = ctx.author.avatar_url)

        em.add_field(name = "Name:", value = member, inline=False)
        em.add_field(name = "ID:", value = member.id, inline=False)
        em.add_field(name = "Created on:", value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p"), inline=False)
        em.add_field(name = "Joined the Sevrer on:", value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"), inline=False)
        em.add_field(name = f"Roles ({len(roles)})", value = " ".join([role.mention for role in roles]), inline=False)
        em.add_field(name = "Top Role:", value = member.top_role.mention, inline=False)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):

        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        channels = text_channels + voice_channels

        em = discord.Embed(
        
            title = f"**ServerInfo Command**",
            description = f"",
            color = 0xD71E8C
        )

        em.set_thumbnail(url = str(ctx.guild.icon_url))
        em.set_footer(text = f"Invoked by: {ctx.author}", icon_url = ctx.author.avatar_url)

        em.add_field(name = "Name:", value = f"{ctx.guild.name}", inline=False)
        em.add_field(name = "ID:", value = f"{ctx.guild.id}", inline=False)
        em.add_field(name = "Created on:", value = ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p"), inline=False)
        em.add_field(name = "Channels:", value = f"{channels} Total, {text_channels} Text, {voice_channels} Voice, {categories} Categories", inline=False)

        em.add_field(name = "Owner:", value = f"{ctx.guild.owner}", inline=True)
        em.add_field(name = "Region:", value = f"{ctx.guild.region}", inline=True)
        em.add_field(name = "Splash:", value = f"{ctx.guild.splash}", inline=True)

        await ctx.send(embed = em, delete_after=120)
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds= None):
        if seconds == None:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send(f"Set the slowmode delay in this channel to 0 seconds!", delete_after=120)
            await ctx.message.delete()

        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!", delete_after=120)
            await ctx.message.delete()

    @slowmode.error
    async def slowmode_error(self, ctx, error):

        if isinstance(error, CheckFailure):
            await ctx.send('You don`t have the permission to use this command!', delete_after=120)
            await ctx.message.delete()

########## Setup ##########

def setup (client):
    client.add_cog(Moderation(client))
