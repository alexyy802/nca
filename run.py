import discord
from discord.ext import commands
import json
import os
import asyncpg
from datetime import datetime
import aiosqlite
import asyncio
import discord 
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = ',',intents=intents)
status=discord.Status.idle
activity=discord.Activity(type=discord.ActivityType.listening, name="The prefix  ( , )")

@bot.event
async def on_ready():
    await bot.change_presence(status=status, activity=activity)
    await bot.db.execute("CREATE TABLE IF NOT EXISTS warnlogs (guild_id BIGINT, member_id BIGINT, warns TEXT[], times DECIMAL[])")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS modlogmute (guild_id BIGINT, member_id BIGINT, mutes TEXT[], times DECIMAL[])")
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')






if __name__ == '__main__':
    for name in os.listdir("./cogs"):
        if name.endswith(".py"):
            bot.load_extension("cogs.{}".format(name[:-3]))



@bot.event
async def on_message(message):
    if message.content in [f"<@{bot.user.id}>", f"<@!{bot.user.id}>"]:
        await message.channel.send(f"""Hi,{message.author.mention} you pinged me 
if you need help type ``,help``""")
    await bot.process_commands(message)
    







async def create_db_pool():
    bot.db = await asyncpg.create_pool(database = "NCA",password = "iloveyou6676112007",user = "postgres")
   



bot.loop.run_until_complete(create_db_pool())
bot.run("ODgxODg4Nzk4MTYwNTkyOTU2.YSzY8g.372KT3JfL4eL8XGVkLE2x0HDsco")
