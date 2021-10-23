import discord
from discord.ext import commands

class Dm(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def dm(self,ctx,user:discord.Member,* ,dm_message):
      try:
       e = discord.Embed(title="Message from admin!")
       e.add_field(name="Message :",value=dm_message)
       await member.send(embed=e)
       await ctx.send('Message Sent :white_check_mark:')
       return
      except:
        await ctx.send('Looks like i could not dm that member :cry:')
        return
      
      
def setup(bot):
  bot.add_cog(Dm(bot))
