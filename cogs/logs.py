import discord
from discord.ext import commands
import random
import datetime


class Logs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        if before.bot:
            return
        try:

            log = self.bot.get_channel(889534432103510127)
                        
            old_roles = " ".join([role.mention for role in before.roles])

            new_roles  =" ".join([role.mention for role in after.roles])

            em = discord.Embed(title ="Member Edited Info ",color = 0xffb432,timestamp = datetime.datetime.utcnow())
            def func(state):
                activity = ""
                if isinstance(state.activities,tuple):
                    for i in state.activities:
                        try:
                            activity =  activity+ i.name+" "
                            
                        except:
                            pass
                        try:
                            activity = activity+"**"+i.title+"**"
                        except:
                            pass
                        activity += "\n"
                else:
                    activity = state.activities[0]
                if activity == "":
                    activity = "None"
                return activity
                
            em.set_author(name = after,icon_url = after.avatar_url)
            if str(before.status).upper() != str(after.status).upper():
                em.add_field(name = "Old Status : ",value = f"Status : {str(before.status).upper()}")
                em.add_field(name = "New Status : ",value = f"Status : {str(after.status).upper()}")
                pass
            elif func(before) != func(after):
                em.add_field(name = "Old Activity : ",value = f"Status : {func(before)}")
                em.add_field(name = "New Activity : ",value = f"Status : {func(after)}")
                pass
            elif before.display_name != after.display_name:
                em.add_field(name = "Old Nickname : ",value = f"Status : {before.display_name}")
                em.add_field(name = "New Nickname : ",value = f"Status : {after.display_name}")
                pass
            elif old_roles!=new_roles:
                em.add_field(name = "Old Roles : ",value = f"Status : {old_roles}")
                em.add_field(name = "New Roles : ",value = f"Status : {new_roles}")
                pass
            
            else:
                return
            await log.send(embed = em)
        except:
            pass
    
    @commands.Cog.listener()
    async def on_message_delete(self,message):

        if message.author.bot:
            return
        log = self.bot.get_channel(889534669643718688)
        embed = discord.Embed(title = "Message Deleted",timestamp = datetime.datetime.utcnow())
        embed.add_field(name="Message",value=message.content,inline=False)
        embed.add_field(name="Author",value=message.author.name,inline=False)
        embed.add_field(name="Channel",value=f"<#{message.channel.id}>",inline=False)
        embed.set_thumbnail(url="https://icons.iconarchive.com/icons/cornmanthe3rd/plex/512/System-recycling-bin-full-icon.png")
        await log.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self,old,new):
        
        if old.author.bot:
            return
        log = self.bot.get_channel(889534669643718688)
        embed = discord.Embed(title = "Message Edited",description = f"[Jump to the Message]({new.jump_url})",timestamp = datetime.datetime.utcnow())
        embed.add_field(name="Old Message",value=old.content)
        embed.add_field(name="New Message",value=new.content)
        embed.add_field(name="Channel",value=f"<#{old.channel.id}>",inline=False)
        embed.add_field(name="Author",value=old.author.name,inline=False)
        embed.set_thumbnail(url="https://th.bing.com/th/id/R66dbcbb7f70864efa5e4e8097e865a28?rik=KbhIVKRoP5CCLw&riu=http%3a%2f%2fwww.recycling.com%2fwp-content%2fuploads%2f2016%2f06%2frecycling-symbol-icon-outline-solid-dark-green.png&ehk=uUs07SqPyEepr2jBZhiGSUkO1QbzTCvEobnhAM%2fddU8%3d&risl=&pid=ImgRaw")
        await log.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self,guild,before,after):
        
        log = self.bot.get_channel(889534819657207848)
        before_emotes = ""
        after_emote = ""
        for i in before:
            name = f"<:{i.name}:{i.id}>"
            before_emotes += name + " "
            
        for i in after:
            name = f"<:{i.name}:{i.id}>"
            after_emote += name + " "
            
        try:
            em = discord.Embed(title ="New Emotes :) available : ",color = 0xffb432)
            em.add_field(name = "Old Server Emotes : ",value = before_emotes)
            em.add_field(name = "New Server Emotes : ",value = after_emote)
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name = self.bot.user,icon_url = self.bot.user.avatar_url)
            await log.send(embed = em)
        except:
            pass


def setup(bot):
    bot.add_cog(Logs(bot))