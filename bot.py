import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply("Привет! Я — твой персональный фитнес-гид. 🚴‍♂️ Введи свой рост в сантиметрах, и начнём!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

