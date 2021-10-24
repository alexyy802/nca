import discord
from discord.ext import commands
import json
import os
import asyncpg
from datetime import datetime
import aiosqlite
import asyncio





intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = ',',intents=intents)

bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="The prefix  ( , )"))
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')




async def update_totals(member):
    invites = await member.guild.invites()

    c = datetime.today().strftime("%Y-%m-%d").split("-")
    c_y = int(c[0])
    c_m = int(c[1])
    c_d = int(c[2])

    async with bot.db.execute("SELECT id, uses FROM invites WHERE guild_id = ?", (member.guild.id,)) as cursor: # this gets the old invite counts
        async for invite_id, old_uses in cursor:
            for invite in invites:
                if invite.id == invite_id and invite.uses - old_uses > 0: # the count has been updated, invite is the invite that member joined by
                    if not (c_y == member.created_at.year and c_m == member.created_at.month and c_d - member.created_at.day < 7): # year can only be less or equal, month can only be less or equal, then check days
                        print(invite.id)
                        await bot.db.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
                        await bot.db.execute("INSERT OR IGNORE INTO joined (guild_id, inviter_id, joiner_id) VALUES (?,?,?)", (invite.guild.id, invite.inviter.id, member.id))
                        await bot.db.execute("UPDATE totals SET normal = normal + 1 WHERE guild_id = ? AND inviter_id = ?", (invite.guild.id, invite.inviter.id))

                    else:
                        await bot.db.execute("UPDATE totals SET normal = normal + 1, fake = fake + 1 WHERE guild_id = ? and inviter_id = ?", (invite.guild.id, invite.inviter.id))

                    return
    
# events
@bot.event
async def on_member_join(member):
    await update_totals(member)
    await bot.db.commit()
        
@bot.event
async def on_member_remove(member):
    cur = await bot.db.execute("SELECT inviter_id FROM joined WHERE guild_id = ? and joiner_id = ?", (member.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        return
    
    inviter = res[0]
    
    await bot.db.execute("DELETE FROM joined WHERE guild_id = ? AND joiner_id = ?", (member.guild.id, member.id))
    await bot.db.execute("DELETE FROM totals WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, member.id))
    await bot.db.execute("UPDATE totals SET left = left + 1 WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, inviter))
    await bot.db.commit()

@bot.event
async def on_invite_create(invite):
    await bot.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (invite.guild.id, invite.inviter.id, invite.uses, 0, 0))
    await bot.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
    await bot.db.commit()
    
@bot.event
async def on_invite_delete(invite):
    await bot.db.execute("DELETE FROM invites WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
    await bot.db.commit()

@bot.event
async def on_guild_join(guild): # add new invites to monitor
    for invite in await guild.invites():
        await bot.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses), VAlUES (?,?,?)", (guild.id, invite.id, invite.uses))
        
    await bot.db.commit()
    
@bot.event
async def on_guild_remove(guild): # remove all instances of the given guild_id
    await bot.db.execute("DELETE FROM totals WHERE guild_id = ?", (guild.id,))
    await bot.db.execute("DELETE FROM invites WHERE guild_id = ?", (guild.id,))
    await bot.db.execute("DELETE FROM joined WHERE guild_id = ?", (guild.id,))

    await bot.db.commit()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.errors.Forbidden):
        await ctx.send("The member has his/her dm's off :no_entry_sign:")
        return
    if isinstance(error, discord.errors.HTTPException):
        await ctx.send("There was an error while trying to send a message to this user.")
        return
    
# commands
@bot.command()
async def invites(ctx, member: discord.Member=None):
    if member is None: member = ctx.author

    # get counts
    cur = await bot.db.execute("SELECT normal, left, fake FROM totals WHERE guild_id = ? AND inviter_id = ?", (ctx.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        normal, left, fake = 0, 0, 0

    else:
        normal, left, fake = res

    total = normal - (left + fake)
    
    em = discord.Embed(
        title=f"Invites for {member.name}#{member.discriminator}",
        description=f"{member.mention} has **{total}** invites in Total!!.",
        timestamp=datetime.now(),
        colour=discord.Colour.orange())
    em.add_field(name=f" **{normal}** invites|, **{left}** left |, **{fake}** fake.",value="\u200b",inline =False)
    em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    await ctx.send(embed=em)
    
async def setup():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("inviteData.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS totals (guild_id int, inviter_id int, normal int, left int, fake int, PRIMARY KEY (guild_id, inviter_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS invites (guild_id int, id string, uses int, PRIMARY KEY (guild_id, id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS joined (guild_id int, inviter_id int, joiner_id int, PRIMARY KEY (guild_id, inviter_id, joiner_id))")
    
    # fill invites if not there
    for guild in bot.guilds:
        for invite in await guild.invites(): # invites before bot was added won't be recorded, invitemanager/tracker don't do this
            await bot.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
            await bot.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (guild.id, invite.inviter.id, 0, 0, 0))
                                 
    await bot.db.commit()


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
    
@bot.command(aliases=["mc"])
async def member_count(ctx):
    a=ctx.guild.member_count
    b=discord.Embed(title=f"Member count",description=f" We have {ctx.guild.member_count} mebers in our server" )
    await ctx.send(embed=b)
    
@bot.command(aliases=["ml"])
async def memberlist(ctx):
        for guild in bot.guilds:
            for member in guild.members:
                embed = discord.Embed(title="Member List's",description= (member))
                await ctx.send(embed=embed)


@bot.slash_command(guild_ids=[853602966379560980])
async def hello(ctx):
    """Say hello to the bot"""  
    await ctx.send(f"Hello {ctx.author}!")



@bot.slash_command(guild_ids=[853602966379560980])
async def ping(ctx):
        """Check the bot latency"""
        embed = discord.Embed(description = f" :ping_pong:  **|** Pong! I have a bot ping of: **{round(bot.latency * 1000)}ms**", colour = discord.Colour.blue())
        embed.set_footer(text = "It's your turn now!")
        await ctx.send(embed=embed)
  










bot.loop.create_task(setup())
bot.run("ODgxODg4Nzk4MTYwNTkyOTU2.YSzY8g.wgmuvOPoGZrvwEnua5da0GoICOA")
asyncio.run(bot.db.close())
