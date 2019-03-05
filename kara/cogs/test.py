import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context


class Test:
    _bot: Bot

    def __init__(self, bot: Bot):
        self._bot = bot

    @commands.command(name="test", brief="dupa")
    async def test(self, ctx: Context):
        await ctx.send(f"Hello, {ctx.author.mention}!")


def setup(bot: Bot):
    bot.add_cog(Test(bot))
