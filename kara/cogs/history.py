from i18n import t
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from json import load, dump
from time import strftime, gmtime


async def load_data():
    with open("data/history.json", "r") as f:
        return load(f)


async def save_data(data):
    with open("data/history.json", "w") as f:
        dump(data, f, indent=2)


class History(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.nick and not after.nick or before.nick == after.nick:
            return

        data = await load_data()
        user_id = str(before.id)
        guild_id = str(before.guild.id)

        # TODO: Add a guild id key to the hist.json file if it doesn't exist
        if user_id not in data[guild_id]:
            data[guild_id][user_id] = []

        data[guild_id][user_id].append([strftime("%A, %d.%m.%Y", gmtime()), after.nick if after.nick else after.name])

        await save_data(data)

    @commands.command(name="history", aliases=["hist"], ignore_extra=True)
    async def history(self, ctx: Context, member: Member = None):
        """mention name id"""
        data = await load_data()

        if not member:
            member = ctx.message.author
        if str(member.id) not in data[str(member.guild.id)]:
            await ctx.send(t("history.no_hist", name=member.name))

        nicks = [f"`{i[0]}`  {i[1]}" for i in data[str(member.guild.id)][str(member.id)]]  # Create a list of nicks

        embed = Embed(description=t("history.title", mention=member.mention), timestamp=ctx.message.created_at)
        embed.add_field(name=t("history.nicks"), value="\n".join(nicks))  # TODO: Add a limit
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(History(bot))
