import discord
from discord.ext import commands



class HelpCommand(commands.HelpCommand):
    def get_ending_note(self):
        return f"Use ,{self.invoked_with} [command] for more info on a command."

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = ", ".join(command.aliases)
            fmt = f"[{command.name}, Aliases: {aliases}]"
            if parent:
                fmt = f"{parent}, {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help!", color=discord.Color.blurple())
        description = self.context.bot.description
        if description:
            embed.description = description

        for cog_, cmds in mapping.items():
            name = "Other Commands" if cog_ is None else cog_.qualified_name
            filtered = await self.filter_commands(cmds, sort=True)
            if filtered:
                value = "\u002C ".join(f"`{c.name}`" for c in cmds)
                if cog_ and cog_.description:
                    value = "{0}\n{1}".format(cog_.description, value)

                embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog_):
        embed = discord.Embed(title="{0.qualified_name} Commands".format(cog_))
        if cog_.description:
            embed.description = cog_.description

        filtered = await self.filter_commands(cog_.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=self.get_command_signature(command),
                value=command.short_doc or "...",
                inline=False,
            )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "...",
                    inline=False,
                )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    send_command_help = send_group_help










def setup(bot: commands.Bot):
    bot.help_command = HelpCommand()