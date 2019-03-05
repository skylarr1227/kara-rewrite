import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context


class Fun:
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="ship")
    async def ship(self, ctx: Context, left: discord.Member, right: discord.Member):
        """Ships two users together"""
        left = left.name[:int(len(left.name) / 1.5)]
        right = right.name[int(len(right.name) / 1.5):]
        await self.bot.say(f"Aww, **{left}{right}** - the cutest couple ever.")

    @commands.command(name="uwu")
    async def uwu(self):
        """UwU"""
        await self.bot.say("https://cdn.discordapp.com/attachments/527591004497510410/529117293729546241/unknown.png")


def setup(bot: Bot):
    bot.add_cog(Fun(bot))
