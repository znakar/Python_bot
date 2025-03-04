import os
from dotenv import load_dotenv
import telebot
from help import commands
from keyboard_markup import markup
import sqlite3 as sq

load_dotenv('BOT_TOKEN.env')

BOT_TOKEN = os.environ.get('BOT_TOKEN')

if BOT_TOKEN is None:
    print('BOT_TOKEN environment variable not set')
else:
    print('BOT_TOKEN environment variable is set')

bot = telebot.TeleBot(BOT_TOKEN)



@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Greetings, there is a buttons you can choose", reply_markup=markup)


@bot.message_handler(commands=['image'])
def send_image(message):
    bot.reply_to(message, "Send me your photo", reply_markup=markup)

    bot.register_next_step_handler(message, handle_photo)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id  # Получаем ID самого большого фото
    weight = message.photo[-1].file_size # Вес изображения
    format = "JPEG" # Предполагаем формат JPEG



    # Запрашиваем имя изображения у пользователя
    bot.reply_to(message, "Please, name your picture")  # Отправляем пользователю подтверждение

    # Регистрируем следующий шаг для получения имени
    bot.register_next_step_handler(message, save_photo, file_id, weight, format)

def save_photo(message, file_id, weight, format):
    name = message.text # Получаем имя от пользователя

    with sq.connect('my_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (file_id, name, weight, format) VALUES (?, ?, ?, ?)",
                       (file_id, name, weight, format))
        conn.commit()

    bot.reply_to(message, f"Photo '{name}' saved in database!")

@bot.message_handler(commands=['help'])
def send_help(message):
    full_message = "What do you want to do?\n\n" + commands # оператор + конкатениреует(объединяет) две строки в одну \n - символ новый строки. Используется для переноса текста на следующую строку

    bot.reply_to(message, full_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'whatever':
        bot.answer_callback_query(call.id, "You pressed the \"Back button\" NOO!")

bot.infinity_polling()

