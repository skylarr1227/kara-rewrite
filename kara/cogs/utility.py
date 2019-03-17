from discord import Embed, Role
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog
from kara.converters import UserConverter
from hastebin import post


class Utility(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="avatar", aliases=["pfp"], brief="Shows a user's avatar.")
    async def avatar(self, ctx: Context, user: UserConverter = None, *args: str):
        """Shows a user's avatar.
        This command accepts these formats:\n
        **Mention**:` {prefix}avatar @Predator`\n
        **Name**:` {prefix}avatar Predator`\n
        **ID**:` {prefix}avatar 195935967440404480`\n
        Note: You can get an avatar of a user not in this guild by using their user ID.
        Note: Use quoes for users with mutli-word names, e.g. `\"User Name\"`"""
        if not user:
            user = ctx.author

        embed: Embed = Embed(description=f"{user.mention}'s avatar")
        embed.set_image(url=user.avatar_url_as(size=2048))
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="compare", aliases=["comp"], brief="Compares two roles.")
    async def compare(self, ctx: Context, role_a: Role, role_b: Role):
        """Compares two roles
        This command accepts these formats:\n
        **Name**:` {prefix}compare RoleA RoleB`\n
        **ID**:` {prefix}compare 412357250401697794 528674655180030002`\n
        **Mixed**:` {prefix}compare RoleA 528674655180030002`\n
        Note: Use quoes for roles with mutli-word names, e.g. `\"Role Name\"`"""
        members_a: set = set(role_a.members)
        members_b: set = set(role_b.members)
        combined: set = set(members_a | members_b)
        combined_names: str = "\n".join(i.name for i in combined)
        both: set = set(members_a & members_b)
        both_names: str = "\n".join(i.name for i in both)
        only_a: set = set(members_a - members_b)
        only_a_names: str = "\n".join(i.name for i in only_a)
        only_b: set = set(members_b - members_a)
        only_b_names: str = "\n".join(i.name for i in only_b)
        no_overlap: set = set(members_b ^ members_a)
        no_overlap_names: str = "\n".join(i.name for i in no_overlap)

        await ctx.trigger_typing()
        embed: Embed = Embed(title="Compare", description=f"Coparing {role_a.mention} with {role_b.mention}")
        embed.add_field(name=f"Members who are in {role_a.name} and {role_b.name}",
                        value=f"**{len(combined)}** members: {post(combined_names.encode('utf-8'))}")
        embed.add_field(name="Members who are in both roles",
                        value=f"**{len(both)}** members: {post(both_names.encode('utf-8'))}")
        embed.add_field(name=f"Members who are only in {role_a.name}",
                        value=f"**{len(only_a)}** members: {post(only_a_names.encode('utf-8'))}")
        embed.add_field(name=f"Members who are only in {role_b.name}",
                        value=f"**{len(only_b)}** members: {post(only_b_names.encode('utf-8'))}")
        embed.add_field(name=f"Members who don't overlap in {role_a.name} and {role_b.name}",
                        value=f"**{len(no_overlap)}** members: {post(no_overlap_names.encode('utf-8'))}")
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Utility(bot))
