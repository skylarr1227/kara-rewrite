from i18n import t, get, set
from random import choice
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog


class Lang(Cog):
    _bot: Bot

    def __init__(self, bot):
        self._bot = bot

    @commands.group(name="lang")
    async def lang(self, ctx: Context):
        if ctx.invoked_subcommand:
            return
        embed: Embed = Embed(title=t("locale.language"))
        embed.add_field(name=t("locale.current"),
                        value=f"**{get('locale')}** {t('flag')}")
        embed.add_field(name=t("locale.available"),
                        value=", ".join(get("available_locales")))
        await ctx.send(embed=embed)

    @lang.command(name="set", brief="Sets the lang.")
    @commands.is_owner()
    async def _set(self, ctx: Context, lang: str):
        if lang not in get("available_locales"):
            return await ctx.send(t("locale.unavailable"))
        set("locale", lang)  # TODO: Overwrite the lang key in config
        await ctx.send(t("locale.set", loc=get("locale")))

    @lang.command(name="get", brief="Returns the key value.")
    async def _get(self, ctx: Context, key: str):
        embed: Embed = Embed(title=t("locale.title", k=key))
        embed.add_field(name=t("locale.translation"),
                        value=t(key, prefix=self._bot.command_prefix,
                                command="lang",
                                name=ctx.author.name,
                                name2=f"{ctx.author.name}_2",
                                id=ctx.author.id,
                                id2=str(ctx.author.id)[::-1],
                                locale=get("locale"),
                                locales=get("available_locales"),
                                k=key,
                                role_id=choice(ctx.guild.roles).id))
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Lang(bot))
