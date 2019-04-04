from i18n import t, get
from random import choice
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog, Command


class Help(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="help", aliases=["h"], hidden=True)
    async def help(self, ctx: Context, name: str = None, subcommand: str = None):
        """name id mention_d"""
        embed: Embed = Embed(title=t("help.help_title"), timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

        if not name:  # show all commands if no args
            for command in self._bot.commands:
                if command.hidden:  # skip if hidden
                    continue
                embed.add_field(name=command.name, value=t(f"doc.brief.{command.name}"), inline=False)
            return await ctx.send(embed=embed)

        if name not in [i.name for i in self._bot.commands]:  # invalid command name given
            return await ctx.send(t("help.not_found", name=name, prefix=self._bot.command_prefix))

        command = next(i for i in self._bot.commands if i.name == name)
        if command.hidden:  # command is hidden
            return await ctx.send(t("help.no_help", name=name, prefix=self._bot.command_prefix))

        try:
            # if subcommand:  # check if command has subcommands
            #     command = command.all_commands[subcommand]  # TODO: Make proper help for subcommands
            embed.add_field(name=t("help.subcommands"), value=", ".join(list(command.all_commands)))
        except AttributeError:
            pass

        embed.title = t("help.command_help_title", name=command.name)
        if command.aliases:  # check if command has aliases
            embed.add_field(name=t("help.aliases"), value=", ".join(command.aliases))

        description = f"{t(f'doc.brief.{command.name}')}\n\n"  # create description, all commands have one

        if command.help:  # command has specified formats, add to description
            global formats
            formats = []
            for i in command.help.split():
                formats.append("• " + t(f'doc.formats.{i}', prefix=self._bot.command_prefix, command=command.name,
                                        name=ctx.author.name, name2=f"{ctx.author.name}_2",
                                        id=ctx.author.id, id2=str(ctx.author.id)[::-1],
                                        role_id=choice(ctx.guild.roles).id) + "\n")
            description += (f"__{t('help.formats')}__:\n"
                            f"{''.join(formats)}\n")

        if t(f"doc.notes.{command.name}") != f"doc.notes.{command.name}":  # command has notes, add to description
            description += (f"__{t('help.notes')}__:\n"
                            f"{t(f'doc.notes.{command.name}')}")

        embed.add_field(name=t("help.description"), inline=False, value=description)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Help(bot))
