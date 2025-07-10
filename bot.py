import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
import openai

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class UserForm(StatesGroup):
    height = State()
    weight = State()
    age = State()
    goal = State()
    habits = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await UserForm.height.set()
    await message.reply("Привет! Я — твой персональный фитнес-гид. 🧠 Поехали!\n\nСкажи свой рост (в см):")

@dp.message_handler(state=UserForm.height)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await UserForm.next()
    await message.reply("Теперь вес (в кг):")

@dp.message_handler(state=UserForm.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await UserForm.next()
    await message.reply("Сколько тебе лет?")

@dp.message_handler(state=UserForm.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserForm.next()
    await message.reply("Цель: похудеть, набрать массу или держать форму?")

@dp.message_handler(state=UserForm.goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await UserForm.next()
    await message.reply("Расскажи о своих привычках: сон, питание, вредные привычки...")

@dp.message_handler(state=UserForm.habits)
async def process_habits(message: Message, state: FSMContext):
    await state.update_data(habits=message.text)
    data = await state.get_data()

    await message.reply("Отлично! Генерирую для тебя план, это займёт 5–10 секунд... ⏳")
    plan = await generate_plan(data)
    await message.reply(plan)
    await state.finish()

async def generate_plan(data: dict) -> str:
    prompt = f"""
Составь подробный месячный план тренировок и питания для человека:
Рост: {data['height']} см
Вес: {data['weight']} кг
Возраст: {data['age']}
Цель: {data['goal']}
Привычки: {data['habits']}

Сделай план понятным, мотивирующим, с разбивкой на дни недели.
"""
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.7,
    )
    return resp.choices[0].text.strip()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
