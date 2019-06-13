import re
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from json import load, dump


async def load_data():
    with open("data/bot_id.json", "r") as f:
        return load(f)


async def save_data(data):
    with open("data/bot_id.json", "w") as f:
        dump(data, f, indent=2)


class JoinListener(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        bot_nick_match = re.match(r"[A-Z][a-z]*(\.[a-z]*)*\d{2,4}", member.name)
        data = await load_data()

        if not bot_nick_match or member.id in data["id"]:
            return

        data["id"].append(member.id)
        await save_data(data)

    @commands.command(name="botlist", hidden=True, ignore_extra=True)
    async def botlist(self, ctx: Context):
        data = await load_data()
        #embed = Embed(tile="Bot ID's", description=data["id"], timestamp=ctx.message.created_at)
        #embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        #await ctx.send(embed=Embed)
        await ctx.send("\n".join([f"`{i}` ({await self._bot.fetch_user(i)})" for i in data["id"]]))

def setup(bot: Bot):
    bot.add_cog(JoinListener(bot))

