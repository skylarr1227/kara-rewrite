from i18n import t
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from kara.entities.database import User, Warn, db
from pony.orm import db_session, select
from datetime import datetime


class Administration(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    # This is temporary, just for testing purposes
    @commands.command(name="query")
    @commands.is_owner()
    async def query(self, ctx: Context, *, query: str):
        with db_session:
            result = db.select(query)
            await ctx.send("\n".join([str(i) for i in result[:]]))

    @commands.command(name="warn")
    @commands.is_owner()
    async def warn(self, ctx: Context, member: Member, *, reason: str):
        with db_session:
            user = User.get(id=str(member.id))
            if user is None:
                user = User(id=str(member.id))

            warn = Warn(given_by=str(ctx.author.id),
                        user=user,
                        reason=reason,
                        when=datetime.now())

            await ctx.send(f"{warn.user.id} warned for *{warn.reason}*")

    @commands.command(name="warns", ignore_extra=True)
    async def warns(self, ctx: Context, member: Member):
        with db_session:
            user = User.get(id=str(member.id))
            if user is None:
                return await ctx.send("No warn entries.")

            warns = select(i for i in user.punishments
                           if isinstance(i, Warn)).without_distinct()

            await ctx.send("\n".join([i.reason for i in warns[:]]))


def setup(bot: Bot):

    bot.add_cog(Administration(bot))
