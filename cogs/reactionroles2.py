import discord
import json
from discord.ext import commands

class Reaction_Roles2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.message_id not in [883190421742821416,889082324199809064, 889164062158626897,895908109652992021]:
            return
        if payload.member.bot:
            pass
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

        else:
            with open('reactrole.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == str(payload.emoji):
                        if str(x["channel_id"]) == str(payload.channel_id):
                            role = discord.utils.get(self.bot.get_guild(
                                payload.guild_id).roles, id=x['role_id'])

                            
                            await payload.member.send(f'\nI have given  you {role} role \nCheck out your roles to check if its their or not')
                            await payload.member.add_roles(role)















def setup(bot):
    bot.add_cog(Reaction_Roles2(bot))








