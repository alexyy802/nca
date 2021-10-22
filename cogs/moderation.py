from os import name
import discord
from discord.ext import commands
import asyncio
import datetime

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def warn_log(self,guild_id,member_id):
        data = await self.bot.db.fetchrow("SELECT * FROM warnlogs WHERE guild_id = $1 AND member_id = $2",guild_id,member_id)
        if not data:
            return []
        return data

    async def warn_entry(self,guild_id,member_id,reason,time):
        data = await self.warn_log(guild_id,member_id)
        if data == []:
            await self.bot.db.execute('INSERT INTO warnlogs (guild_id, member_id, warns, times) VALUES ($1,$2,$3,$4)',guild_id, member_id, [reason], [time])
            return
        warns = data[2]
        times = data[3]
        warns.append(reason)
        times.append(time)
        await self.bot.db.execute("UPDATE warnlogs SET times = $1, warns = $2 WHERE guild_id = $3 AND member_id = $4",times,warns,guild_id,member_id)


    async def modlog_mute_log(self,guild_id,member_id):
        data = await self.bot.db.fetchrow


    @commands.command(aliases = ['m'],description="Mutes the specified user.")
    @commands.has_permissions(manage_messages=True)
    async def mute(self,ctx, member: discord.Member, *, reason=' Reason not provided'):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        
        await ctx.send(f"""{ctx.author.mention} has muted {member.mention}
Reason: {reason}""")
        await member.add_roles(mutedRole, reason=reason)
        Embed3 = discord.Embed(title="You are Muted kido ", description=f"{member.mention} was muted"
        , colour=discord.Colour.blue())
        Embed3.add_field(name="Reason:", value={reason}, inline=False)
        await member.send(embed=Embed3)


    @commands.command(aliases = ['um'],description="Unmutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self,ctx, member: discord.Member,*,reason='Reason not provided'):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        Embed4 = discord.Embed(title="You are unmuted KiDo", description=f"{ctx.author.mention}unmuted{member.mention}"
        , colour=discord.Colour.blue())
        Embed4.add_field(name="Reason", value=reason, inline=False)
        await member.send(embed=Embed4)
        Embed5 = discord.Embed(title="Umutes", description=f"""{ctx.author.mention}unmuted {member.mention}
    Reason: {reason}  """,colour=discord.Colour.blue())
        
        await ctx.send(embed=Embed5)



    @commands.command(aliases = ['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, user: discord.Member, *, reason=None):
        
        await ctx.send(f"""{user} have been kicked sucessfully
Reason: {reason}""")
        embed = discord.Embed(title='You are Kicked from the server')
        embed.add_field(name="Reason:", value=f'{reason}')
        await user.send(embed=embed)
        await user.kick(reason=reason)



    @commands.command(aliases = ['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, user: discord.Member, *, reason=None):
        await ctx.send(f"{user} have been bannned sucessfully\nReason: {reason}")
        embed = discord.Embed(title=f'{ctx.guild.name}:',description='You are banned from the server' )
        embed.add_field(name='Reason',value=f"{reason}")
        embed.add_field(name="Moderator  Who baned you:",value=f"{ctx.author.mention}",inline=True)
        await user.send(embed=embed)
        await user.ban(reason=reason)
        

    @commands.command(aliases = ['ub'])
    async def unban(self,ctx, member:discord.User ,*,reason="Not provided"):
        banned_users = await ctx.guild.bans()
        
        for ban_entry in banned_users:
            user = ban_entry.user
  
            if member.id == user.id:
                await ctx.guild.unban(user)
                await ctx.send(f"{user} have been unbanned sucessfully\nReason:{reason}")
                return


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self,ctx,amount = 5):
            await ctx.message.delete()
            await ctx.channel.purge(limit = amount)
            Embed7 = discord.Embed(title = f"{amount} messages were cleared",color = discord.Color.green())
            await ctx.send(embed = Embed7, delete_after = 10.0)



    @commands.command(aliases = ['chn'])
    @commands.has_permissions(manage_roles = True)
    async def changenickname(self,ctx,*,nick):
        await ctx.send(f'Nickname was  successfully changed for {ctx.mention} ')
        try:
            await ctx.edit(nick=nick)
        except:
            embed = discord.Embed(title=f'Error')
            embed.add_field(name=f'Reason.1',value=f"cannot change nickname for {member.mention} because my role isnt above {member.mention}'s role if you need to change {member.mention}'s nickname make my role above {member.mention}'s role!")
            return await ctx.send(embed=embed)
        await ctx.send(f'Nickname was  successfully changed for {ctx.mention} ')
    
    @changenickname.error
    async def changenickname_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f' Error ', description = 'Oopss seems you dont have permisions to do it', colour = discord.Colour.blue())
            await ctx.send(embed=embed)

    @commands.command()
    async def tempmute(self,ctx, member: discord.Member, time:int,d, *, reason=None):
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.add_roles(role)

                embed = discord.Embed(title="Muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
                embed.add_field(name="reason:", value=reason, inline=False)
                embed.add_field(name="time left for the mute:", value=f"{time}{d}", inline=False)
                await member.send(embed=embed)
                await ctx.send(f"""Tempmuted {member.mention} 
Reason: {reason}
Time: {time}{d} """)

                if d == "s":
                    await asyncio.sleep(time)

                if d == "m":
                    await asyncio.sleep(time*60)

                if d == "h":
                    await asyncio.sleep(time*60*60)

                if d == "d":
                    await asyncio.sleep(time*60*60*24)

                await member.remove_roles(role)

                embed = discord.Embed(title="unmute (temp) ", description=f"unmuted -{member.mention} ", colour=discord.Colour.blue())
                try:
                    await member.send(embed=embed)
                except:
                    pass
                await ctx.send(f'Unmuted {member.mention}')






    @commands.command(aliases = ['W'])
    
    async def warn(self,ctx,member:discord.Member,*,reason = "No reason provided"):
        if member==ctx.author or member==self.bot.user:
            return await ctx.send("You cant warn your self or the bot lol")




        if not ctx.author.top_role.position>member.top_role.position:
            return await ctx.send('You cannot warn higher user above you or the member with same heirarchy level')

        await self.warn_entry(ctx.guild.id,member.id,reason,ctx.message.created_at.timestamp())
        await ctx.send(f"{ctx.author.name} has warned {member.name} \nReason : {reason} ")

        data = await self.warn_log(ctx.guild.id,member.id)
        count = len(data[3])
        embed = discord.Embed(title=f"Warned by {ctx.author.name}",color = discord.Colour.blue(),timestamp = datetime.datetime.utcnow())
        embed.add_field(name="Reason",value=reason)
        embed.add_field(name="Total Warn's",value=f"**{count}**warns")
        embed.set_thumbnail(url = ctx.author.avatar.url)
        try:
            await member.send(embed=embed)
        except:
            pass


    @commands.command(name='lock')
    @commands.has_permissions(manage_channels = True)
    async def lockdown(self,ctx):
        guild = ctx.guild
        Verifedrole = discord.utils.get(guild.roles, name="Verified")
        await ctx.channel.set_permissions(Verifedrole, send_messages=False)
        await ctx.send( ctx.channel.mention + " ***is now in lockdown.***",delete_after = 3)
        await ctx.message.delete()

    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self,ctx):
        guild = ctx.guild
        Verifedrole = discord.utils.get(guild.roles, name="Verified")
        await ctx.channel.set_permissions(Verifedrole, send_messages=True)
        await ctx.send(ctx.channel.mention + " ***has been unlocked.***",delete_after = 3)
        await ctx.message.delete()



def setup(bot):
    bot.add_cog(ModerationCommands(bot))  

