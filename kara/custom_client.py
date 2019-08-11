import discord.ext.commands.errors as cerrors
from i18n import t
from discord import Embed, Color
from discord.ext.commands import Bot, Context
from kara.entities.config import Config
from kara.default_cog import DefaultCog


class CustomClient(Bot):
    config: Config

    def __init__(self, config, **options):
        super().__init__(command_prefix=config.prefix, **options)
        self.config = config
        self.remove_command("help")
        DefaultCog.reload_extensions(self)

    @staticmethod
    def startup(self):
        self.run(self.config.token)

    async def on_ready(self):
        print("-" * 20, flush=True)
        print(f"Logged in as {self.user.name}", flush=True)
        print(f"Lang: {self.config.lang}", flush=True)
        print(f"Cogs: {', '.join(self.config.start_cogs)}", flush=True)
        print(f"Commands: {', '.join([i.name for i in self.commands])}",
              flush=True)
        print(f"Command prefix: {self.command_prefix}", flush=True)
        print("-" * 20, flush=True)
        await DefaultCog.reload_presence(self)

    async def on_command_error(self, ctx: Context, exception: Exception):
        embed: Embed = Embed(title=t("errors.error"),
                             color=Color.red(),
                             timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

        try:
            raise exception
        except cerrors.CommandNotFound:
            return
        except cerrors.NotOwner:
            embed.description = t("errors.not_owner")
        except cerrors.BadArgument:
            embed.description = t("errors.bad_argument")
        except cerrors.MissingRequiredArgument:
            embed.description = t("errors.missing_arguments")
        except cerrors.TooManyArguments:
            embed.description = t("errors.too_many_arguments")
        except cerrors.ConversionError:
            embed.description = t("errors.conversion")
        except Exception:
            embed.description = str(exception)
            print(exception, flush=True)

        await ctx.send(embed=embed)
