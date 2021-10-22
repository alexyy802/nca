
import discord
from discord.ext import commands
from contextlib import redirect_stdout
from typing import Union, Optional
import time 
import aiohttp
import random
import urllib
import asyncio
import re
from io import BytesIO
from discord import Embed, Member
from datetime import datetime,timedelta
from psutil import Process



class UserCommands(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(aliases = ['av'])
    async def avatar(self,ctx, * ,member : discord.Member=None):
        if not member:
            member = ctx.message.author
            

        Embed6 = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        Embed6.set_author(name=f"Avatar of{member}")
        Embed6.set_image(url=member.avatar.url)
        Embed6.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=Embed6)



    @commands.command()
    async def ping(self, ctx):
        """Check the bot latency"""
        embed = discord.Embed(description = f" :ping_pong:  **|** Pong! I have a bot ping of: **{round(self.bot.latency * 1000)}ms**", colour = discord.Colour.blue())
        embed.set_footer(text = "It's your turn now!")
        await ctx.send(embed=embed)
    
    @commands.command(aliases = ['msg'])
    async def message(self,ctx,channel:discord.TextChannel=None,*,message=None):
        channel = channel or self.ctx.channel
        await ctx.message.delete()
        await channel.send(message)


    @commands.command(aliases = ['msgem'])
    async def messageembed(self,ctx,channel:discord.TextChannel=None ,title='Self Roles KiDo',*,description=None ):
        channel = channel or self.ctx.channel
        embed = discord.Embed(title=title, description=description)
        await channel.send(embed=embed)

    @commands.command(aliases = ['o'])
    async def owner(self,ctx):
        await ctx.send('I was made by my Great Grant Master DCG_Dark_Boy#0001')



    @commands.command(name='msgdm')
    async def message_dm(self,ctx,member:discord.Member,*,message=None):
        await ctx.message.delete()
        await member.send(f'`` {message}``'+ f'\n||Note: i wont read replys in Dms ,Reply Me in Server LAMOOO||')


    @commands.command(aliases = ["gsp"])
    async def ghost_ping(self,ctx ,channel:discord.TextChannel=None,*,message=None):
        channel = channel or self.ctx.channel
        await channel.send(f"<@{message}>",delete_after = 1)      
        await ctx.message.delete()

    @commands.command(aliases=["whois"])
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed = Embed(title="User information",
                      colour=target.colour,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=target.avatar.url)

        fields = [("Name", str(target), True),
                  ("ID", target.id, True),
                  ("Bot?", target.bot, True),
                  ("Top role", target.top_role.mention, True),
                  ("Status", str(target.status).title(), True),
                  ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
                  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Boosted", bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    
    @commands.command(aliases=["si"])
    async def server_info(self, ctx):
        embed = Embed(title="Server information",
                      colour=ctx.guild.owner.colour,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon.url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Region", ctx.guild.region, True),
                  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Members", len(ctx.guild.members), True),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Banned members", len(await ctx.guild.bans()), True),
                  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)






    @commands.command(aliases=['info', 'stats', 'status'])
    async def show_bot_stats(self, ctx):
        embed = Embed(title="Bot stats",
                      colour=ctx.author.colour)
                      

        embed.set_thumbnail(url=self.bot.user.avatar.url)
        proc = Process
        with proc.oneshot:
            uptime = timedelta(seconds=time()-proc.create_time())
            cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [
            ("Bot version", self.bot.VERSION, True),
            ("Python version", python_version(), True),
            ("discord.py version", discord_version, True),
            ("Uptime", uptime, True),
            ("CPU time", cpu_time, True),
            ("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
            ("Users", f"{self.bot.guild.member_count:,}", True)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(aliases=["mc"])
    async def member_count(ctx):
        a=ctx.guild.member_count
        b=discord.Embed(title=f"Member count",description=f" We have {ctx.guild.member_count} mebers in our server" )
        await ctx.send(embed=b)
        
    @commands.command(aliases=["ml"])
    async def memberlist(ctx):
            for guild in bot.guilds:
                for member in guild.members:
                    embed = discord.Embed(title="Member List's",description= (member))
                    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserCommands(bot))