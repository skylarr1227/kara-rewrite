import re
import discord.ext.commands.errors as cerrors
from discord.ext.commands import Converter, Context, Bot
from discord import User
from discord.utils import get


class UserConverter(Converter):
    async def convert(self, ctx: Context, argument: str) -> User:
        user_id_match = re.match(r"<@(!|)(?P<id>\d+)>", argument)
        bot: Bot = ctx.bot

        if not user_id_match:
            try:
                member = get(ctx.message.guild.members, name=argument)
                user_id = member.id
            except:
                user_id = argument
        else:
            user_id = user_id_match.group("id")

        try:
            return await bot.get_user_info(user_id=user_id)
        except:
            raise cerrors.BadArgument
