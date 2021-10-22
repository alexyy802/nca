import discord
import asyncpraw
import random
from discord.ext import commands

class Memes(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot



    @commands.command(aliases = ['meme'])
    #@commands.cooldown(1, 10,  commands.BucketType.member)
    async def memes(self,ctx):
        

        reddit = asyncpraw.Reddit(client_id = "CmnZiPb6hPaBUV-DsVL62Q",
                                client_secret = "ZGTtP_7XS8wUkwj76UYmTxSPz4IBHQ",
                                username = "DARKZONAI", 
                                password = "riskysteve93936676",
                                user_agent = 'pythonpraw')

        subreddit = await reddit.subreddit("meme")
        top = subreddit.top(limit=50)
        all_subs = []
        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)
        while random_sub.over_18:
            random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        em = discord.Embed(title=f'{name}', colour=discord.Colour.blue(), timestamp=ctx.message.created_at)

        em.set_image(url=url)
        em.set_author(name=ctx.message.author, icon_url=ctx.author.avatar.url)
        em.set_footer(text=f'Meme for {ctx.message.author.name}')
        await ctx.send(content = f'**Here is your meme:** ',embed = em)
        return




def setup(bot):
    bot.add_cog(Memes(bot)) 