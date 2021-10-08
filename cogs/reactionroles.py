import discord
import json
from discord.ext import commands

class Reaction_Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id not in [889105972851773521, 888436179169595472, 889092830050537513]:
            return

        if payload.member.bot:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        send_message = False

        for reaction in message.reactions:
            if str(reaction.emoji) != str(payload.emoji):
                await message.remove_reaction(reaction.emoji, payload.member)
                send_message = True


        if send_message:
            await payload.member.send("You can choose only 1 role  from the message so i unreacted the previous one\n if you need the ryt one react that\nso please dont misuse roles\n **What i mean is i have given you only the last reacted one**")
        else:
            with open('reactrole.json', 'r') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == str(payload.emoji):
                        if str(x["channel_id"]) == str(payload.channel_id):
                            role = discord.utils.get(self.bot.get_guild(
                                payload.guild_id).roles, id=x['role_id'])

                            await payload.member.add_roles(role)
                            await payload.member.send(f"I have given you **{role}** role. Check out your roles to check if it's there or not.")



    @commands.Cog.listener()  
    async def on_raw_reaction_remove(self,payload):
        guild = self.bot.get_guild(payload.guild_id) or await self.bot.fetch_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.bot:
            pass
            

        else:
            with open('reactrole.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == str(payload.emoji):
                        if str(x["channel_id"]) == str(payload.channel_id):
                            guild = self.bot.get_guild(payload.guild_id)
                            role = discord.utils.get(guild.roles, id=x['role_id'])
                            member = guild.get_member(payload.user_id)


                            await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)                        
                            await member.send(f'\nI have removed  {role} role from you ')
                            print("removed")



    @commands.command(aliases=["rr"])
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def reactrole(self,ctx,channel:discord. TextChannel,msgid, emoji, role: discord.Role):        
        msg = await channel.fetch_message(msgid)

        with open('reactrole.json') as json_file:
            data = json.load(json_file)

            new_react_role = {'role_name': role.name, 
            'role_id': role.id,
            'emoji': emoji,
            'message_id': msg.id,
            'channel_id': channel.id}

            data.append(new_react_role)

        with open('reactrole.json', 'w') as f:
            json.dump(data, f, indent=4)
            await msg.add_reaction(emoji)











def setup(bot):
    bot.add_cog(Reaction_Roles(bot))