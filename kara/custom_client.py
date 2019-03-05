import discord
import discord.ext.commands.errors as cerrors
from discord.ext.commands import Bot, Context
from kara.entities.status import from_filename
from kara.entities import Config
from kara.default_cog import DefaultCog


class CustomClient(Bot):
    config: Config

    def __init__(self, config, **options):
        super().__init__(command_prefix=config.prefix, **options)
        self.config = config
        self.remove_command("help")
        DefaultCog.reload_extensions(self)

    @staticmethod
    def startup(self) -> None:
        self.run(self.config.token)

    async def on_ready(self) -> None:
        name = self.user.name
        print("-" * len(name))
        print(f"Logged in as {name}")
        print(f"Command prefix: {self.command_prefix}")
        print("-" * len(name))

        status = from_filename("data/status.json")
        return await self.change_presence(activity=status)

    async def on_command_error(self, context: Context, exception) -> None:
        try:
            raise exception
        except cerrors.NotOwner:
            await context.send(f"You don't have permissions to use this command {context.author.mention}")
        except cerrors.BadArgument:
            await context.send(f"A bad argument was given {context.author.mention}")
        except cerrors.MissingRequiredArgument:
            await context.send(f"You are missing some required argument(s) {context.author.mention}")
        except cerrors.TooManyArguments:
            await context.send(f"Too many arguments {context.author.mention}")
        except cerrors.CommandNotFound:
            return
        except Exception:
            await context.send(f"A {type(exception)} exception occurred: [{exception}]")
            print(exception)
            print(type(exception))
