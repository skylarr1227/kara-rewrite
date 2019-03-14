import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from kara.entities.status import get_status
from time import time
from datetime import timedelta

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
                print(e)
        for extension in bot.config.start_cogs:
            bot.load_extension(f"kara.cogs.{extension}")
        if not any([isinstance(cog, DefaultCog) for cog in bot.cogs.values()]):
            bot.add_cog(DefaultCog(bot))
        print(f"Reloaded commands: {[command.name for command in bot.commands]}")

    @staticmethod
    def reload_presence(bot: Bot):
        status = get_status("data/status.json")
        return bot.change_presence(activity=status)

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: Context):
        DefaultCog.reload_extensions(self._bot)
        await ctx.send("Reloaded all extensions!")

    @commands.command(name="reloadpresence", hidden=True)
    @commands.is_owner()
    async def reloadpresence(self, ctx: Context):
        DefaultCog.reload_presence(self._bot)
        await ctx.send("Reloaded the presence!")

    @commands.command(name="uptime", hidden=True)
    async def uptime(self, ctx: Context):
        current_timestamp = time()
        difference = int(round(current_timestamp - start_timestamp))
        embed: discord.Embed = discord.Embed(title="Uptime", description=str(timedelta(seconds=difference)))
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(DefaultCog(bot))
