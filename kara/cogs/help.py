import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog


class Help(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="help", aliases=["h"], brief="Shows all available commands.", hidden=True)
    async def help(self, ctx: Context, name: str = None):
        """Shows all available commands."""
        embed: discord.Embed = discord.Embed(title="Help")
        command: discord.ext.commands.Command

        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

        if not name:  # all commands, no args
            for command in self._bot.commands:
                if command.hidden:
                    continue
                embed.add_field(name=command.name, value=command.brief, inline=False)
            return await ctx.send(embed=embed)

        if name not in [i.name for i in self._bot.commands]:  # invalid command name given
            return await ctx.send(f"Command **{name}** not found. Type `{self._bot.command_prefix}help` for more info.")

        command = next(i for i in self._bot.commands if i.name == name)
        if command.hidden:  # command is hidden
            return await ctx.send(f"Help for **{name}** not found. Type `{self._bot.command_prefix}help` for more info.")

        embed.title = f"Help for the {command.name} command"
        if command.aliases:  # command has aliases
            embed.add_field(name="Aliases", value=command.aliases)
        embed.add_field(name="Description", value=command.help.replace("{prefix}", self._bot.command_prefix))
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Help(bot))