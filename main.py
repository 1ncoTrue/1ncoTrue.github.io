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
import aiosqlite

TOKEN = "8482137840:AAFb90M1s80TyXjgm9AJSlxZp_BbpuaydDE"
OPERATORS_CHAT_ID = -1002949153158

dp = Dispatcher()

def builder_main() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    builder.button(text='📱 Открыть приложениe', web_app=WebAppInfo(url="https://1ncotrue.github.io/"))
    return builder.as_markup()

async def create_db():
    async with aiosqlite.connect('database.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL UNIQUE,
                            username TEXT,
                            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        await db.commit()
    
async def user_exists(user_id):
    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
        user = await cursor.fetchone()
        return user is not None

async def add_user(user_id, username):
    async with aiosqlite.connect('database.db') as db:
        await db.execute('''INSERT OR REPLACE INTO users 
                          (user_id, username) 
                          VALUES (?, ?)''',
                          (user_id, username))
        await db.commit()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = message.from_user
    user_id = user.id
    username = user.username
    
    await add_user(user_id, username)

    await message.answer(f'Здесь можно увидеть актуальное расписание на сегодня.\n' 
                         f'Да да расписание для всего ИСИТА уже здесь.\n'
                         f'Мб скоро сделаю для всего первого курса.\n'
                         f'❗❗❗Внимательно проверяйте расписание, если нашли ошибку пишите в чат боту', reply_markup=builder_main(), parse_mode=ParseMode.HTML)

@dp.message()
async def forward_to_operators(message: Message, bot: Bot):
    await bot.send_message(
        OPERATORS_CHAT_ID,
        f"Сообщение от @{message.from_user.username or message.from_user.id}:\n{message.text}"
    )

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())