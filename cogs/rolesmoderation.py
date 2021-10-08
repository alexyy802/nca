import discord
from discord.ext import commands

class UserroleCheckerCommands(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot



    @commands.command(aliases=['cr'])
    @commands.has_permissions(manage_roles=True) # Check if the user executing the command can manage roles
    async def create_role(self,ctx, *, name):
        guild = ctx.guild
        await guild.create_role(name=name)
        await ctx.send(f'Role `{name}` has been created')

    @commands.command(aliases=['dr'])
    async def delete_role(self,ctx, role_name):
        #find role object
        role_object = discord.utils.get(ctx.message.guild.roles, name=role_name)
        #delete role
        await role_object.delete()
        await ctx.send(f'Role ``{role_name}`` has been deleted succesfully.')

    @commands.command(aliases = ['a'])

    async def add(self,ctx, member: discord.Member, role: discord.Role):
        try:
            role = discord.utils.get(ctx.guild.roles, name=role.name)
            await member.add_roles(role)
            await ctx.send(f"Successfully added {role.mention} role  to {member.mention}")
        except Exception as e:
            print(e)




    @add.error
    async def add_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f' Error ', description = 'Oopss seems you dont have permisions to do it', colour = discord.Colour.blue())
            await ctx.send(embed=embed)



    @commands.command(aliases = ['rm'])

    async def remove(self,ctx, member: discord.Member, role: discord.Role):
        try:
            role = discord.utils.get(ctx.guild.roles, name=role.name)
            await member.remove_roles(role)
            await ctx.send(f"Successfully removed {role.mention} role from {member.mention}")
        except Exception as e:
            print(e)




def setup(bot):
    bot.add_cog(UserroleCheckerCommands(bot))