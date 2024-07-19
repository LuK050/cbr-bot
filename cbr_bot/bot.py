import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import database
from cbr_bot.handlers.exchange_command import exchange_command_route
from cbr_bot.handlers.rates_command import rates_command_route
from cbr_bot.handlers.start_command import start_command_route
from cbr_bot.tasks.update_rates import update_rates

load_dotenv()
_TOKEN: str = os.getenv("TOKEN")
print(_TOKEN)


async def on_startup():
    logging.info("Bot started")


async def main():
    bot = Bot(token=_TOKEN)
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_routers(
        start_command_route,
        rates_command_route,
        exchange_command_route,
    )

    asyncio.create_task(update_rates(), name="update_rates")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
