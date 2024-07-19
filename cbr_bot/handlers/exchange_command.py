from typing import Optional

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from cbr_bot.database import redis

exchange_command_route = Router()


@exchange_command_route.message(Command("exchange"))
async def command_exchange(message: Message, command: CommandObject):
    currency_from, currency_to, count = command.args.split()
    currency_from, currency_to = currency_from.upper(), currency_to.upper()
    count: float = float(count)

    if currency_from == "RUB":
        value_from: float = 1
    else:
        value_from: Optional[bytes] = await redis.get(f"currency:{currency_from}")

        if value_from is None:
            await message.answer("")
            return

        value_from: float = float(value_from.decode("utf-8"))

    if currency_to == "RUB":
        value_to: float = 1
    else:
        value_to: Optional[bytes] = await redis.get(f"currency:{currency_to}")

        if value_to is None:
            await message.answer("")
            return

        value_to: float = float(value_to.decode("utf-8"))

    await message.answer(f"""
*Перевод валюты:*

`{count}` {currency_from}  =  `{round(value_from / value_to * count, 4)}` {currency_to}
    """, parse_mode="Markdown")
