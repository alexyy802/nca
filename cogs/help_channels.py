from os import name
import discord
from discord.ext import commands
from asyncio import TimeoutError
class HelpChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    
    @commands.command()
    async def helper(self, ctx, lang=None,*,description=None) -> None:
        lang = ['python', 'javascript','java','html or css','other']
        response = []
        helper_role = None
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        if not lang or not description:
            embed = discord.Embed(title=f'Which language you need help with',description='``python``,``javascript``,``java``,``html or css``,``other``')

            await ctx.send(embed=embed,delete_after = 10.0)
            
            try:
                lr = await self.bot.wait_for("message", check=check, timeout=60)
            except TimeoutError:
                await ctx.send('Lamoo you didnt reponde in time, use the helper command again to ask help')
            else:
                response.append(lr.content.lower())
            
            embed = discord.Embed(title='Description',description='Please give us a short description regarding your help about ``10-1000``charchters')
            await ctx.send(embed=embed)
            try:
                des = await self.bot.wait_for("message", check=check, timeout=120)
            except TimeoutError:
                await ctx.send('Lamoo you didnt reponde in time, use the helper command again to ask help')
            else:
                response.append(des.content.lower())
            if response[0].lower() == 'python':
                helper_role = 870908069784195082
            elif response[0].lower() == 'javascript':
                helper_role = 870942301181067264
            elif response[0].lower() == 'java':
                helper_role = 870942354998185984
            elif response[0].lower() == 'html or css':
                helper_role = 870942264074076220
            elif response[0].lower() == 'other':
                helper_role = 882494954197381130
            channel = discord.utils.get(ctx.guild.channels, id= 870912555294539857)
            embed = discord.Embed(title=f'{response[0]} help',description=f'[click here](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}) to help {ctx.author.mention}') 
            embed.add_field(name='description',value=response[1])
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await channel.send(content=f"<@&{helper_role}>",embed=embed)
            embed = discord.Embed(title='Your help ticket has been submited',description=f'To veiw your question response [click here](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id})')
            embed.add_field(name=f'Language which you need help with  ',value=response[0],inline=False)
            embed.add_field(name='Question you asked as a help  ',value=response[1],inline=False)

            await ctx.author.send(embed=embed)
            embed = discord.Embed(title='Request has been submited',description="""Request has been submited regarding your dought
Our Coding helper's will help you in a moment 
Please keep in mind that our helpers are human and may not be available immediately. """)
            await ctx.send(embed=embed)
            category = discord.utils.get(ctx.guild.channels, id=882194404859846676)
            await ctx.channel.move(category=category, end=True)

    @commands.command(name='cht')
    async def closehthread(self, message):
            category = self.bot.get_channel(882194351193747537)
            await message.channel.move(category=category, end=True)
            embed = discord.Embed(title='Thread Closed',description="""The thread has been closed and has been moved to avilable help channels catagory
if you need more help regarding programing just type ``,helper`` """)
            embed.set_footer(text=f"Requested by {message.author}", icon_url=message.author.avatar.url)
            await message.channel.send(embed=embed)
            
       
    
def setup(bot):
    bot.add_cog(HelpChannels(bot))