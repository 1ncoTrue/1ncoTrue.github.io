import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8482137840:AAFb90M1s80TyXjgm9AJSlxZp_BbpuaydDE"

dp = Dispatcher()

def builder_main() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    builder.button(text='📱 Открыть приложениe', web_app=WebAppInfo(url="https://1ncotrue.github.io/"))
    return builder.as_markup()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Здесь можно увидеть актуальное расписание на сегодня.\n 
                            Пока расписание только для группы ДЭ 24-25,
                            но в планах добавить весь ИСИТ', reply_markup=builder_main(), parse_mode=ParseMode.HTML)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())