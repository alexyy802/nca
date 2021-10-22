import discord
import json
from discord.ext import commands
emojis = {
        888436179169595472: {
            "🧑\u200d🦰": 870942533121896449,
            "👩\u200d🦰": 870942616181698600,
            "\u274c": 870943152125644850,
        },
        889092830050537513: {
            "1\ufe0f\u20e3": 870942589828890634,
            "2\ufe0f\u20e3": 870943314168393738,
            "3\ufe0f\u20e3": 870943451464744990,
            "4\ufe0f\u20e3": 870943590484959252,
        },
        889105972851773521: {
            "🟥": 870943795091488769,
            "🟩": 870944011244945408,
            "🟨": 870944051959066655,
            "🟧": 870944105541275689,
            "🟪": 870944173015052348,
            "🟫": 870944224227508275,
            "⬜": 870944242007175188
        }    
    }
class Reaction_Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()  
    async def on_raw_reaction_add(self,payload: discord.RawReactionActionEvent):
        if payload.message_id not in emojis:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        for r in message.reactions:
            # If the user has reacted, is not a bot, and has the reaction doesn't equal the payload one
            if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                await message.remove_reaction(r.emoji, payload.member) 
                await payload.member.send("You can only react one from this message.")


        for role in self.bot.get_guild(payload.guild_id).roles:
            if role.id == emojis[payload.message_id][payload.emoji.name]:
                await payload.member.add_roles(role)
                await payload.member.send(f"Gave you a shiny **{role}** role")
                break

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



    @commands.command(aliases=["rt"])
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def roletest(self,ctx,channel:discord. TextChannel,msgid, emoji, role: discord.Role):        
        msg = await channel.fetch_message(msgid)
        with open('rt.json') as json_file:
            data = json.load(json_file)

            new_react_role = {'role_name': role.name, 
            'role_id': role.id,
            'emoji': emoji,
            'message_id': msg.id,
            'channel_id': channel.id}

            data.append(new_react_role)

        with open('rt.json', 'w') as f:
            json.dump(data, f, indent=4)
            await msg.add_reaction(emoji)






def setup(bot):
    bot.add_cog(Reaction_Roles(bot))