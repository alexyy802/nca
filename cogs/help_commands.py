import discord
from discord.ext import commands



class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def help(self,ctx):
        embed = discord.Embed(title='Help Commands',description='```Use ,help<space>[command name] to get more information on that command name```',color = ctx.author.color, timestamp=ctx.message.created_at)
        embed.add_field(name='Moderation Commands',value = '``kick``,``ban``,``unban``,``mute``,``unmute``,``tempmute``,``clear``,``changenickname``,``role``',inline=False)
        embed.add_field(name='Helper Command',value='``helper``',inline=False)
        embed.add_field(name='User Commands',value = '``meme``,``avatar``,``ping``',inline=False)
        embed.add_field(name='Music Commands',value='``join``,``leave``,``play``,``skip``,``pause``,``resume``',inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @help.command()
    async def role(self,ctx):
        embed = discord.Embed(title="Role Help KiDo",inline=False,color = ctx.author.color, timestamp=ctx.message.created_at)
        embed.add_field(name="**Commands**",value="• **create** \n[Aliases = cr ]--Type ``,cr<space>rolename`` to create a new role. \n• **delete**\n[Aliases = dr]--Type ``,dr<space>rolename``  to delete the  role. \n• **add**\n[Aliases = a ]--Type ``,a<space>@member.mention<space>@role.mention`` to add a  role to mentioned user. \n• **remove**\n[Aliases= rm ]``,rm<space>@member.mention<space>@role.mention`` to remove a  role from the  mentioned user.")
        await ctx.reply(embed=embed)

    @help.command()
    async def helper(self,ctx):
        em = discord.Embed(title="Help for ``helper`` command ",description="Helper commands are used to get help regarding coding related stuffs\n You can say ``,helper ``  in sepcified channel \nYou can know all channels in <#870912068147097631>",color = ctx.author.color, timestamp=ctx.message.created_at)
        em.add_field(name="How to use it ??", value="You can say ``,helper`` in sepcifiedhelp channels \nwhich is mentioned in <#870912068147097631>  to get help",inline=False)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=em)



    @help.command()
    async def kick(self,ctx):
        em = discord.Embed(title="Command: Kick Help",description="```To kick a user you should follow the given steps below ```",color = ctx.author.color, timestamp=ctx.message.created_at)
        em.add_field(name="Attribute:",value=",kick<space> ``@member.mention`` <space>reason")
        em.add_field(name="Explanation:",value=":small_blue_diamond: ``,`` is the prefix\n:small_blue_diamond: ``kick`` is the command\n:small_blue_diamond: ``@member.mention`` this line means you should either mention the user or use the users id\n:small_blue_diamond: ``reason`` means you need to provid the reason to kick the member ")
        em.set_footer( icon_url=ctx.author.avatar.url)
        em.set_author(name=ctx.message.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=em)


    @help.command()
    async def ban(self,ctx):
        em = discord.Embed(title="Command: Ban Help",description="```To ban a user you should follow the given steps below ```",color = ctx.author.color, timestamp=ctx.message.created_at)
        em.add_field(name="Attribute:",value=",ban<space> ``@member.mention`` <space>reason")
        em.add_field(name="Explanation:",value=":small_blue_diamond: ``,`` is the prefix\n:small_blue_diamond: ``ban`` is the command\n:small_blue_diamond: ``@member.mention`` this line means you should either mention the user or use the users id\n:small_blue_diamond: ``reason`` means you need to provid the reason to ban the member ")
        em.set_footer( icon_url=ctx.author.avatar.url)
        em.set_author(name=ctx.message.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=em)

    @help.command()
    async def unban(self,ctx):
        em = discord.Embed(title="Command: Unban Help",description="```To unban a user you should follow the given steps below ```",color = ctx.author.color, timestamp=ctx.message.created_at)
        em.add_field(name="Attribute:",value=",unban<space> ``@member.mention`` <space>reason")
        em.add_field(name="Explanation:",value=":small_blue_diamond: ``,`` is the prefix\n:small_blue_diamond: ``unban`` is the command\n:small_blue_diamond: ``@member.mention`` this line means you should either mention the user or use the users id\n:small_blue_diamond: ``reason`` means you need to provid the reason to unban the member ")
        em.set_footer( icon_url=ctx.author.avatar.url)
        em.set_author(name=ctx.message.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(HelpCommands(bot))