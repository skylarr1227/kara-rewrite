from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from kara.entities.status import get_status
from time import time
from datetime import timedelta
from i18n import t

start_timestamp = time()


class DefaultCog(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @staticmethod
    def reload_extensions(bot: Bot):
        for extension in list(bot.extensions):
            try:
                bot.unload_extension(extension)
            except Exception as e:
                print(e, flush=True)
        for extension in bot.config.start_cogs:
            bot.load_extension(f"kara.cogs.{extension}")
        if not any([isinstance(cog, DefaultCog) for cog in bot.cogs.values()]):
            bot.add_cog(DefaultCog(bot))
        print(f"Reloaded commands: {sorted([command.name for command in bot.commands])}", flush=True)

    @staticmethod
    def reload_presence(bot: Bot):
        status = get_status("data/status.json")
        return bot.change_presence(activity=status)

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: Context):
        DefaultCog.reload_extensions(self._bot)
        await ctx.send(t("reload_commands"))

    @commands.command(name="reloadpresence", hidden=True)  # this doesn't really work
    @commands.is_owner()
    async def reloadpresence(self, ctx: Context):  # TODO: Fix reloadpresence command
        DefaultCog.reload_presence(self._bot)
        await ctx.send(t("reload_status"))

    @commands.command(name="uptime", hidden=True)
    async def uptime(self, ctx: Context):
        current_timestamp = time()
        difference = int(round(current_timestamp - start_timestamp))
        embed: Embed = Embed(title="Uptime",
                             description=str(timedelta(seconds=difference)),
                             timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ping", hidden=True)
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong! {round(self._bot.latency * 1000)}ms")


def setup(bot: Bot) -> None:
    bot.add_cog(DefaultCog(bot))
