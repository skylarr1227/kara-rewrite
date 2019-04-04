from i18n import t
from discord import Embed, Role
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from kara.converters import UserConverter
from hastebin import post


class Utility(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="avatar", aliases=["pfp", "av"], ignore_extra=True)
    async def avatar(self, ctx: Context, user: UserConverter = None):
        """mention name id"""
        if not user:
            user = ctx.author

        embed: Embed = Embed(description=t("avatar", mention=user.mention), timestamp=ctx.message.created_at)
        embed.set_image(url=user.avatar_url_as(size=2048))
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="role", ignore_extra=True)
    async def role(self, ctx: Context, role: Role):
        """name id"""
        embed: Embed = Embed(description=t("role.title", mention=role.mention),
                             color=role.color,
                             timestamp=ctx.message.created_at)
        embed.add_field(name=t("role.name"), value=role.name)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name=t("role.created_at"), value=role.created_at.ctime(), inline=True)
        embed.add_field(name=t("role.color"), value=f"Hex: {role.color}\nRGB: {role.color.to_rgb()}", inline=True)
        embed.add_field(name=t("role.users"), value=str(len(role.members)), inline=True)
        embed.add_field(name=t("role.mentionable"), value=role.mentionable)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="compare", aliases=["comp"], ignore_extra=True)
    async def compare(self, ctx: Context, role_a: Role, role_b: Role):
        """name id mixed"""
        members_a: set = set(role_a.members)
        members_b: set = set(role_b.members)

        combined: set = set(members_a | members_b)
        both: set = set(members_a & members_b)
        only_a: set = set(members_a - members_b)
        only_b: set = set(members_b - members_a)
        no_overlap: set = set(members_b ^ members_a)

        combined_names: str = "\n".join(i.name for i in combined)
        both_names: str = "\n".join(i.name for i in both)
        only_a_names: str = "\n".join(i.name for i in only_a)
        only_b_names: str = "\n".join(i.name for i in only_b)
        no_overlap_names: str = "\n".join(i.name for i in no_overlap)

        await ctx.trigger_typing()
        embed: Embed = Embed(title=t("compare.title"), description=t("compare.description", a=role_a.mention,
                                                                     b=role_b.mention),
                             timestamp=ctx.message.created_at)
        embed.add_field(name=t("compare.combined", a=role_a.name, b=role_a.name),
                        value=t("compare.members", amount=len(combined), url=post(combined_names.encode('utf-8'))))
        embed.add_field(name=t("compare.both"),
                        value=t("compare.members", amount=len(both), url=post(both_names.encode('utf-8'))))
        embed.add_field(name=t("compare.only", role=role_a.name),
                        value=t("compare.members", amount=len(only_a), url=post(only_a_names.encode('utf-8'))))
        embed.add_field(name=t("compare.only", role=role_b.name),
                        value=t("compare.members", amount=len(only_b), url=post(only_b_names.encode('utf-8'))))
        embed.add_field(name=t("compare.no_overlap", a=role_a.name, b=role_b.name),
                        value=t("compare.members", amount=len(no_overlap), url=post(no_overlap_names.encode('utf-8'))))
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Utility(bot))
