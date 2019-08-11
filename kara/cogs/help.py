from i18n import t
from random import choice
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog


class Help(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="help", aliases=["h", "halp"], hidden=True)
    async def help(self, ctx: Context, name: str = None):
        """name id mention_d"""

        embed: Embed = Embed(title=t("help.help_title"),
                             timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        out_text = ""

        # If no args given, list all commands
        if not name:
            for command in self._bot.commands:  # TODO: Add support for aliases
                if command.hidden:  # skip if hidden
                    continue
                out_text += f"`{self._bot.command_prefix}{command.name}` - " \
                            f"{t(f'doc.brief.{command.name}')}\n\n"
            embed.description = out_text
            return await ctx.send(embed=embed)

        # Check if invalid command name given
        if name not in [i.name for i in self._bot.commands]:
            return await ctx.send(t("help.not_found", name=name,
                                    prefix=self._bot.command_prefix))

        command = next(i for i in self._bot.commands if i.name == name)
        # If the command is hidden, treat it like it has no help message
        if command.hidden:
            return await ctx.send(t("help.no_help", name=name,
                                    prefix=self._bot.command_prefix))

        try:
            embed.add_field(name=t("help.subcommands"),
                            value=", ".join(list(command.all_commands)))
        except AttributeError:
            pass

        embed.title = t("help.command_help_title", name=command.name)
        if command.aliases:  # check if command has aliases
            embed.add_field(name=t("help.aliases"),
                            value=", ".join(command.aliases))

        # Get the description
        description = f"{t(f'doc.brief.{command.name}')}\n\n"

        # If the command has info about syntax specified in its docstring, add
        # it to the embed
        if command.help:
            formats = []
            for i in command.help.split():
                syntax = t(f'doc.formats.{i}',
                           prefix=self._bot.command_prefix,
                           command=command.name, name=ctx.author.name,
                           name2=f"{ctx.author.name}_2", id=ctx.author.id,
                           id2=str(ctx.author.id)[::-1],
                           role_id=choice(ctx.guild.roles).id)
                formats.append("• " + syntax + "\n")
            description += (f"__{t('help.formats')}__:\n"
                            f"{''.join(formats)}\n")

        # If the command has notes, add them to the description
        if t(f"doc.notes.{command.name}") != f"doc.notes.{command.name}":
            description += (f"__{t('help.notes')}__:\n"
                            f"{t(f'doc.notes.{command.name}')}")

        embed.add_field(name=t("help.description"), inline=False,
                        value=description)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Help(bot))
