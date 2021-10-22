import discord
import json
from discord.ext import commands

class Welcomemsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(853602966966501428)
        channel2 = self.bot.get_channel(853606717824303124)
        channel3 = self.bot.get_channel(853604724846624818)
        channel4 = self.bot.get_channel(862629281682948106)
        mc = str(member.guild.member_count)
        em = discord.Embed(title=f"Welcome  to NeXus Official Server",description=":small_red_triangle_down: Make sure\n:small_blue_diamond: Read:- <#853604724846624818> follow them.\n:small_blue_diamond: Read:- <#862629281682948106> react to emojis to view channel\n:small_blue_diamond: Use:- <#853606717824303124> for chatting with other members\n:small_blue_diamond: Read <#870912068147097631> To get help regarding your coding help")
        em.set_image(url="https://www.google.com/url?sa=i&url=https%3A%2F%2Ftenor.com%2Fsearch%2Fanimated-welcome-gifs&psig=AOvVaw3WbwACfHO1CUpr5vFgESNy&ust=1633755368148000&source=images&cd=vfe&ved=0CAkQjRxqFwoTCPDi7ZWDuvMCFQAAAAAdAAAAABAD")
        em.add_field(name="☆━━━━━━━━━━━━━━━━━━━━━━━━━━☆",value="\u200b",inline=False)
        em.add_field(name="User Registered - 🔹", value=f"{member.mention}",inline=False)
        em.add_field(name="Now we have:", value=f"{mc} members",inline=True)
        em.set_author(name="NeXus Welcome's you", icon_url="https://cdn.discordapp.com/attachments/857143597132677141/895891970046717972/New_Project_19.png")
        em.set_thumbnail(url=member.avatar.url)
        em.set_footer(text=f"Be active in the server and have fun 💖", icon_url="https://cdn.discordapp.com/attachments/857143597132677141/895891970046717972/New_Project_19.png")
        await channel.send(embed=em)  
        await channel2.send(f"Hey Everyone \nLets welcome our new user {member.mention}\nhope you enjoy in the server\nNow we have: **{mc}** members")
        await channel3.send(f"{member.mention}", delete_after = 1)
        await channel4.send(f"{member.mention}", delete_after = 1)
        try:
            await member.send("🔻 Make sure\n🔹 React:-to chat in  channels, click 👉 <#862629281682948106>  to get verified or else you cant talk in the server \n🔹 please read <#853604724846624818>\n If any issues like cant talk or smthing else \n DM <@!862186182242861077> and explain your issue we will help\nInvite your friend using the link below \nhttps://discord.gg/pEmrd7J448")
        except:
            pass



    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = self.bot.get_channel(854722331687911434)
        mc = str(member.guild.member_count)
        await channel.send(f"Bad news **{member.mention}** just left the server 😪\nI hope he had a great time here\nNow we have only **{mc}  members** :sob:")














def setup(bot):
    bot.add_cog(Welcomemsg(bot))
