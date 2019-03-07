import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog


class DefaultCog(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @staticmethod
    def reload_extensions(bot: Bot) -> None:
        for extension in list(bot.extensions):
            try:
                bot.unload_extension(extension)
            except Exception as e:
                print(e)
        for extension in bot.config.start_cogs:
            bot.load_extension(f"kara.cogs.{extension}")
        if not any([isinstance(cog, DefaultCog) for cog in bot.cogs.values()]):
            bot.add_cog(DefaultCog(bot))
        print(f"Reloaded commands: {[command.name for command in bot.commands]}")

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: Context):
        DefaultCog.reload_extensions(self._bot)
        await ctx.send("Reloaded all extensions!")


def setup(bot: Bot) -> None:
    bot.add_cog(DefaultCog(bot))
