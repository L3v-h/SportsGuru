import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Логирование
logging.basicConfig(level=logging.INFO)

# FSM-хранилище
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Класс для состояний (шагов)
class UserForm(StatesGroup):
    height = State()
    weight = State()
    age = State()
    goal = State()
    habits = State()

# Старт
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await UserForm.height.set()
    await message.reply("Привет! Давай подберём тебе персональный план 🧠\n\nСначала скажи свой рост (в см):")

# Рост
@dp.message_handler(state=UserForm.height)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await UserForm.next()
    await message.reply("А теперь твой вес (в кг):")

# Вес
@dp.message_handler(state=UserForm.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await UserForm.next()
    await message.reply("Отлично! Сколько тебе лет?")

# Возраст
@dp.message_handler(state=UserForm.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserForm.next()
    await message.reply("Какая твоя цель? (например: похудеть, набрать массу, держать форму):")

# Цель
@dp.message_handler(state=UserForm.goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await UserForm.next()
    await message.reply("Расскажи о своих привычках. Например: как питаешься, спишь, есть ли вредные привычки.")

# Привычки
@dp.message_handler(state=UserForm.habits)
async def process_habits(message: Message, state: FSMContext):
    await state.update_data(habits=message.text)
    data = await state.get_data()

    # Здесь пока просто подведём итоги (в будущем — генерация через OpenAI)
    summary = (
        f"✅ Вот что ты ввёл:\n"
        f"Рост: {data['height']} см\n"
        f"Вес: {data['weight']} кг\n"
        f"Возраст: {data['age']}\n"
        f"Цель: {data['goal']}\n"
        f"Привычки: {data['habits']}\n\n"
        f"⏳ Жди... Сейчас будет сгенерирован план!"
    )
    await message.reply(summary)

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
