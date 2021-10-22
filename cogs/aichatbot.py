import discord
from discord.ext import commands
import aiohttp
class AichatBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self,message):
        if self.bot.user == message.author:
         return
       
        if message.channel.id == 870920056337489970 or message.channel.id == 893119708650418217:
            msg = message.content
            server = 'main'
            key = '27W4MCerv06T'
            header = {"Authorization": key}
            master = 'NeXus_Coder_X'
            bot = 'NCA'
            comp = 'The NeXus Coding Acadamy'
            email = 'uh cant provide lol'
            
            params = {'message':msg, 'server': server,'bot_name':bot,'bot_master':master,'bot_company':comp,'bot_email':email}
            async with aiohttp.ClientSession(headers=header) as session:
                async with session.get(f'https://api.pgamerx.com/v5/ai', params=params) as resp:
                
                    text = await resp.json()
                    await message.channel.trigger_typing()
                    await message.reply(text[0]["response"],allowed_mentions=discord.AllowedMentions(users=False,roles=False,everyone=False))
        else:
            pass       
       

        
        





def setup(bot):
    bot.add_cog(AichatBot(bot))

