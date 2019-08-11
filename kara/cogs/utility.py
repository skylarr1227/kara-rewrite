from i18n import t
from discord import Embed, Role
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from kara.converters import UserConverter


# def pastebin(text: str) -> str:
#     if text == "":
#         return ""
#     request_data = {"api_dev_key": "9a6f459f60b5f6d695ae8af0e88e3cf5",
#                     "api_option": "paste",
#                     "api_paste_private": 1,
#                     "api_paste_code": text}
#     return requests.post("https://pastebin.com/api/api_post.php",
#                          data=request_data).text


class Utility(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="avatar", aliases=["pfp", "av"], ignore_extra=True)
    async def avatar(self, ctx: Context, user: UserConverter = None):
        """mention name id"""

        if not user:
            user = ctx.author

        embed: Embed = Embed(description=t("avatar", mention=user.mention),
                             timestamp=ctx.message.created_at)
        embed.set_image(url=user.avatar_url_as(size=2048))
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="role", ignore_extra=True)
    async def role(self, ctx: Context, role: Role):
        """role_name role_id role_mixed"""

        # members = "\n".join([f"{i.name}#{i.discriminator}" for i in role.members])
        embed: Embed = Embed(description=t("role.title", mention=role.mention),
                             color=role.color,
                             timestamp=ctx.message.created_at)
        embed.add_field(name=t("role.name"),
                        value=role.name)
        embed.add_field(name="ID",
                        value=role.id,
                        inline=True)
        embed.add_field(name=t("role.created_at"),
                        value=role.created_at.ctime(),
                        inline=True)
        embed.add_field(name=t("role.color"),
                        value=f"Hex: {role.color}\nRGB: {role.color.to_rgb()}",
                        inline=True)
        embed.add_field(name=t("role.users"),
                        value=str(len(role.members)),
                        inline=True)  # TODO: Fix hastebin
        embed.add_field(name=t("role.mentionable"),
                        value=role.mentionable)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="compare", aliases=["comp"], ignore_extra=True)
    async def compare(self, ctx: Context, role_a: Role, role_b: Role):
        """name_d id_d mixed"""

        members_a = set(role_a.members)
        members_b = set(role_b.members)

        combined: set = members_a | members_b
        both: set = members_a & members_b
        only_a: set = members_a - members_b
        only_b: set = members_b - members_a
        no_overlap: set = members_b ^ members_a

        # Currently off, because hastebin.com died and I am still looking
        # for an unlimited and easy paste service
        # TODO: Fix hastebin
        # combined_names = "\n".join(f"{i.name}#{i.discriminator}" for i in combined)
        # both_names = "\n".join(f"{i.name}#{i.discriminator}" for i in both)
        # only_a_names = "\n".join(f"{i.name}#{i.discriminator}" for i in only_a)
        # only_b_names = "\n".join(f"{i.name}#{i.discriminator}" for i in only_b)
        # no_overlap_names = "\n".join(f"{i.name}#{i.discriminator}" for i in no_overlap)

        await ctx.trigger_typing()
        embed = Embed(title=t("compare.title"),
                      description=t("compare.description",
                                    a=role_a.mention,
                                    b=role_b.mention),
                      timestamp=ctx.message.created_at)
        embed.add_field(name=t("compare.combined",
                               a=role_a.name, b=role_a.name),
                        value=t("compare.members", amount=len(combined),
                                url="Hastebin off"))
        embed.add_field(name=t("compare.both"),
                        value=t("compare.members", amount=len(both),
                                url="Hastebin off"))
        embed.add_field(name=t("compare.only", role=role_a.name),
                        value=t("compare.members", amount=len(only_a),
                                url="Hastebin off"))
        embed.add_field(name=t("compare.only", role=role_b.name),
                        value=t("compare.members", amount=len(only_b),
                                url="Hastebin off"))
        embed.add_field(name=t("compare.no_overlap", a=role_a.name,
                               b=role_b.name),
                        value=t("compare.members", amount=len(no_overlap),
                                url="Hastebin off"))
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Utility(bot))
