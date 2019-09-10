from discord.ext.commands import Converter, Context, Bot
from discord.ext.commands.errors import BadArgument
from discord import Guild, TextChannel, Message
import re


class MessageLinkConverter(Converter):
    message_link_regex = r"(https:\/\/)(canary\.|ptb\.|)discordapp.com\/" \
                         r"channels\/(?P<guild>\d{18})\/(?P<channel>" \
                         r"\d{18})\/(?P<message>\d{18})$"

    async def convert(self, ctx: Context, argument: str) -> Message:
        match = re.match(self.message_link_regex, argument)
        if not match:
            raise BadArgument
        bot: Bot = ctx.bot

        guild: Guild = bot.get_guild(int(match.group("guild")))
        if not guild:
            raise BadArgument

        channel: TextChannel = guild.get_channel(int(match.group("channel")))
        if not channel or not isinstance(channel, TextChannel):
            raise BadArgument

        message: Message = \
            await channel.fetch_message(int(match.group("message")))
        if not message:
            raise BadArgument

        return message
