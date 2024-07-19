from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

start_command_route = Router()


@start_command_route.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await message.answer("""
👋 *Привет!*

Этот бот выполнен в качестве тестового задания Волычевым Кириллом. Он позволят отслеживать текущие курсы валют и переводить одну валюту в другую   
    """, parse_mode="Markdown")
