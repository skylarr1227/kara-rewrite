import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from typing import Optional


class Utility(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="avatar", aliases=["pfp"], brief="Shows a user's avatar.")
    async def avatar(self, ctx: Context, user: Optional[discord.User], *args: Optional[str]):
        """Shows a user's avatar.
        This command accepts these formats:\n
        **Mention**:` {prefix}avatar @Predator`\n
        **Name**:` {prefix}avatar Predator`\n
        **ID**:` {prefix}avatar 195935967440404480`\n
        Note: You can get an avatar of a user not in this guild by using their user ID."""
        if not user:
            user = await self._bot.get_user_info(args[0])

        embed: discord.Embed = discord.Embed(description=f"{user.mention}'s avatar")
        embed.set_image(url=user.avatar_url_as(size=1024))
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Utility(bot))
