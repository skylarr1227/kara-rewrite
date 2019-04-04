import discord.ext.commands.errors as cerrors
from i18n import t
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
        name = self.user.name
        print("-" * len(name), flush=True)
        print(f"Logged in as {name}", flush=True)
        print(f"Lang: {self.config.lang}", flush=True)
        print(f"Cogs: {self.config.start_cogs}", flush=True)
        print(f"Command prefix: {self.command_prefix}", flush=True)
        print("-" * len(name), flush=True)
        await DefaultCog.reload_presence(self)

    async def on_command_error(self, ctx: Context, exception: Exception):
        try:
            raise exception
        except cerrors.NotOwner:
            await ctx.send(t("errors.not_owner", mention=ctx.author.mention))
        except cerrors.BadArgument:
            await ctx.send(t("errors.bad_argument", mention=ctx.author.mention))
        except cerrors.MissingRequiredArgument:
            await ctx.send(t("errors.missing_arguments", mention=ctx.author.mention))
        except cerrors.TooManyArguments:
            await ctx.send(t("errors.too_many_arguments", mention=ctx.author.mention))
        except cerrors.CommandInvokeError:
            if any(i in exception.__str__() for i in ["Unknown User", "Invalid Form Body"]):
                await ctx.send(t("errors.user_not_found", mention=ctx.author.mention))
        except cerrors.CommandNotFound:
            return
        except Exception:
            await ctx.send(t("errors.exception", mention=ctx.author.mention, exception=exception))
            print(exception, flush=True)
            print(type(exception), flush=True)
