import os
import sqlite3 as sq
import asyncio
import logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from SQLite import init_db, save_photo
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from help import commands
from keyboard_markup import markup
from aiogram import F
from dotenv import load_dotenv

# Логирование
logging.basicConfig(level=logging.INFO)
logging.warning('Code is working...')

load_dotenv('BOT_TOKEN.env')

BOT_TOKEN = os.environ.get('BOT_TOKEN')



if BOT_TOKEN is None:
    print('BOT_TOKEN environment variable not set')
else:
    print('BOT_TOKEN environment variable is set')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()




# Определение состояний FSM
class PhotoStates(StatesGroup):
    waiting_for_photo_name = State() # Состояние ожидания имени фото

# Обработчик команды /start и /hello
@dp.message(CommandStart())
@dp.message(Command("hello"))
async def send_welcome(message: Message):
    await message.answer( "Greetings, there is a buttons you can choose", reply_markup=markup)

# Обработчик команды /image
@dp.message(Command("image"))
async def send_image(message: Message):
    await message.answer("Send me your photo", reply_markup=markup)


# Обработчик для получения фото
@dp.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id  # Получаем ID самого большого фото
    weight = message.photo[-1].file_size # Вес изображения
    format = "JPEG" # Предполагаем формат JPEG


# Сохраняем данные в FSM
    await state.update_data(file_id=file_id, weight=weight, format=format)


    # Запрашиваем имя изображения у пользователя
    await message.answer ("Please, name your picture")  # Отправляем пользователю подтверждение

    # Переключаемся в состояние ожидания имени
    await state.set_state(PhotoStates.waiting_for_photo_name)

@dp.message(PhotoStates.waiting_for_photo_name)
async def save_photo_handler(message: Message, state: FSMContext):
    name = message.text

    # Получаем данные из FSM
    data = await state.get_data()
    file_id = data['file_id']
    weight = data['weight']
    format = data['format']

    # Сохраняем данные в базу данных
    save_photo(file_id, name, weight, format)

    await message.answer(f"Photo '{name}' saved in database!")


    await state.clear()

@dp.message(Command("help"))
async def send_help(message):
    full_message = "What do you want to do?\n\n" + commands # оператор + конкатениреует(объединяет) две строки в одну \n - символ новый строки. Используется для переноса текста на следующую строку

    await message.answer(full_message, reply_markup=markup)


@dp.callback_query(F.data == "whatever")
async def handle_query(callback: CallbackQuery):
        await callback.answer("You pressed the \"Back button\" NOO!")


async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

