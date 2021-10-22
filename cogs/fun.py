import discord
from discord.ext import commands
import time 
import aiohttp
from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
import asyncio
import discord
from discord.embeds import Embed
from discord.ext import commands
import random
from discord.utils import get
import os
import wonderwords
import datetime
import re
class Fun(commands.Cog):
  def __init__(self,bot):
    self.bot = bot






 

  @command(name="slap", aliases=["hit"])
  async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
    await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")

  @slap_member.error
  async def slap_member_error(self, ctx, exc):
    if isinstance(exc, BadArgument):
      await ctx.send("I can't find that member.")

  @command(name="echo", aliases=["say"])
  @cooldown(1, 15, BucketType.guild)
  async def echo_message(self, ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

  @command(name="fact")
  async def animal_fact(self, ctx, animal: str):
    if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
      fact_url = f"https://some-random-api.ml/facts/{animal}"
      image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

      async with request("GET", image_url, headers={}) as response:
        if response.status == 200:
          data = await response.json()
          image_link = data["link"]

        else:
          image_link = None

      async with request("GET", fact_url, headers={}) as response:
        if response.status == 200:
          data = await response.json()

          embed = Embed(title=f"{animal.title()} fact",
                  description=data["fact"],
                  colour=ctx.author.colour)
          if image_link is not None:
            embed.set_image(url=image_link)
          await ctx.send(embed=embed)

        else:
          await ctx.send(f"API returned a {response.status} status.")

    else:
      await ctx.send("No facts are available for that animal.")





  @commands.command()
  async def typerace(self, ctx):
      """Who's the fastest typer here? Check your WPM (words per minute)"""
      emojified = ''

      sentence = wonderwords.RandomSentence().sentence().replace(".","")
      length = len(sentence.split())
      formatted = re.sub(r'[^A-Za-z ]+', "", sentence).lower()
        
      for i in formatted:
          if i == ' ':
              emojified += '   '
          else:
              emojified += ':regional_indicator_{}: '.format(i)
      sent = await ctx.send(f"{emojified}.")

      def check(msg):
          return msg.content.lower() == sentence.lower()
      try:
          s = await self.bot.wait_for('message', timeout=60.0, check=check)
      except asyncio.TimeoutError:
          await ctx.send(embed = discord.Embed(description = "No one answered Correct in time.", color = discord.Colour.red()))
      else:
            
          time =  str(datetime.datetime.utcnow() - sent.created_at)
          time_format = time[:-5][5:]
          if time_format[0] == '0':
              time_format = time_format[1:]
            
          embed = discord.Embed(description = f"{s.author.mention} Completed the typerace in **{time_format}** seconds.", color=random.choice(self.colors))
          time_in_mins = float(time_format)/60
          embed.add_field(name = "WPM (Words Per Minute) : ", value = int(length/time_in_mins))
          await ctx.send(embed = embed)














def setup(bot):
    bot.add_cog(Fun(bot))