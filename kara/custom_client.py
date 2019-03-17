import discord.ext.commands.errors as cerrors
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
        print(f"Command prefix: {self.command_prefix}", flush=True)
        print("-" * len(name), flush=True)
        await DefaultCog.reload_presence(self)

    async def on_command_error(self, ctx: Context, exception: Exception):
        try:
            raise exception
        except cerrors.NotOwner:
            await ctx.send(f"You don't have permissions to use this command {ctx.author.mention}")
        except cerrors.BadArgument:
            await ctx.send(f"A bad argument was given {ctx.author.mention}")
        except cerrors.MissingRequiredArgument:
            await ctx.send(f"You are missing some required argument(s) {ctx.author.mention}")
        except cerrors.TooManyArguments:
            await ctx.send(f"Too many arguments {ctx.author.mention}")
        except cerrors.CommandInvokeError:
            if any(i in exception.__str__() for i in ["Unknown User", "Invalid Form Body"]):
                await ctx.send(f"User not found {ctx.author.mention}")
        except cerrors.CommandNotFound:
            return
        except Exception:
            await ctx.send(f"An exception occurred: [{exception}]")
            print(exception, flush=True)
            print(type(exception), flush=True)
