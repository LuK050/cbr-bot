from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from cbr_bot.database import redis

rates_command_route = Router()


@rates_command_route.message(Command("rates"))
async def rates_start(message: Message):
    last_update = (await redis.get("last_update")).decode("utf-8")
    text: str = f"*Курсы валют на {last_update}*:\n\n"

    async for i in redis.scan_iter("currency:*"):
        rate: str = (await redis.get(i)).decode("utf-8")
        code: str = i.decode("utf-8").split(":")[1]
        text += f"`1` {code}  =  `{rate}` RUB\n"

    await message.answer(text, parse_mode="Markdown")
