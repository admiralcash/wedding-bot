from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = "8118288915:AAFetk_yAXr517sDSuG6NZ2yFi96q-ETvoU"
ADMIN_ID = 318677172  # Телеграм ID организатора

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Список фото ID
PHOTO_IDS = [
    "AAMCAgADGQEBxq37Z5ud5B6CXi7slU3qf_Mzj1lvcnsAAghuAAJUTuBIigTVuYm2AzABAAdtAAM2BA",
    "AAMCAgADGQEBxq5TZ5ue3HZk18lBvi-f8PbtMKFRwzYAAiluAAJUTuBIegOfV6nETpoBAAdtAAM2BA",
    "AAMCAgADGQEBxq5oZ5ue6n7KvKI8a651oCVfjw2BEXgAAixuAAJUTuBINxAc6s1cR2oBAAdtAAM2BA",
    "AAMCAgADGQEBxq54Z5ufEvMrro6Fz5HWbr6mXqj4x1IAAjFuAAJUTuBIxFuQG_5YdKoBAAdtAAM2BA",
    "AAMCAgADGQEBxq57Z5ufGBrMKydlrY7XDlABXD4EheYAAjJuAAJUTuBIOBsc5sJj64wBAAdtAAM2BA",
    "AAMCAgADGQEBxq6KZ5ufPaicgL3RRnzbwGESoqPWz54AAjtuAAJUTuBIBOx-bjDTcrYBAAdtAAM2BA",
    "AAMCAgADGQEBxq6OZ5ufUJ2AlIaCymTFE47SzUHiusMAAkBuAAJUTuBInQHldAOFVOsBAAdtAAM2BA"
]

# Хранилище ответов пользователей
user_data = {}

def send_question(chat_id, question, buttons, next_step):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for button in buttons:
        markup.add(KeyboardButton(button))
    msg = bot.send_message(chat_id, question, reply_markup=markup)
    bot.register_next_step_handler(msg, next_step)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    
    for photo_id in PHOTO_IDS[:3]:
        bot.send_photo(chat_id, photo_id)
    
    bot.send_message(chat_id, "📍Локация: Forest Glamp https://2gis.ru/ufa/geo/70000001081557905/55.265181,55.122961 (предусмотрены домики для ночевки🛏 )\n\n"
                              "🚌 Трансфер - Предварительное время 13:30, длительность 1 час 40 минут. Обратно на следующий день к 11:30\n\n"
                              "⏳ Тайминг свадьбы - 15:30 - Фуршет, 16:00 - Свадебная церемония, 16:40 - Банкет, 23:00 - Завершение торжества")
    
    for photo_id in PHOTO_IDS[3:]:
        bot.send_photo(chat_id, photo_id)
    
    send_question(chat_id, "Ты придёшь на свадьбу?", ["Да", "Нет"], process_attendance)

def process_attendance(message):
    chat_id = message.chat.id
    user_data[chat_id]['attendance'] = message.text
    send_question(chat_id, "Будешь с +1?", ["Да", "Нет"], process_plus_one)

def process_plus_one(message):
    chat_id = message.chat.id
    user_data[chat_id]['plus_one'] = message.text
    send_question(chat_id, "Остаешься ли с ночевкой?", ["Да", "Нет"], process_stay)

def process_stay(message):
    chat_id = message.chat.id
    user_data[chat_id]['stay'] = message.text
    send_question(chat_id, "Тебе нужен трансфер?", ["Да, в обе стороны", "Только на свадьбу", "Только со свадьбы", "Нет, приеду на машине"], process_transfer)

def process_transfer(message):
    chat_id = message.chat.id
    user_data[chat_id]['transfer'] = message.text
    send_question(chat_id, "Какое меню выберешь?", ["Мясо", "Рыба"], process_menu)

def process_menu(message):
    chat_id = message.chat.id
    user_data[chat_id]['menu'] = message.text
    send_question(chat_id, "Выбери напитки", ["Шампанское", "Красное вино", "Белое вино", "Мартини", "Крепкий алкоголь", "Безалкогольные напитки"], process_drinks)

def process_drinks(message):
    chat_id = message.chat.id
    user_data[chat_id]['drinks'] = message.text
    msg = bot.send_message(chat_id, "Какие есть пожелания/вопросы?")
    bot.register_next_step_handler(msg, process_comments)

def process_comments(message):
    chat_id = message.chat.id
    user_data[chat_id]['comments'] = message.text
    summary = f"✅ Новый ответ:\n\n"
    for key, value in user_data[chat_id].items():
        summary += f"{key}: {value}\n"
    bot.send_message(ADMIN_ID, summary)
    bot.send_message(chat_id, "Спасибо за участие!\n\nЕсли допустили ошибку – просто нажмите /start и пройдите опрос заново. Ссылка на свадебный чат: https://t.me/+YnMBjkthhZ1mN2Qy")

@bot.message_handler(commands=['notify'])
def notify_users(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(ADMIN_ID, "Введите сообщение для всех гостей:")
        bot.register_next_step_handler(msg, broadcast_message)

def broadcast_message(message):
    text = message.text
    for user_id in user_data.keys():
        try:
            bot.send_message(user_id, text)
        except:
            continue
    bot.send_message(ADMIN_ID, "Сообщение отправлено всем гостям!")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    data = request.get_json()
    print(f"📩 Получены данные от Telegram: {data}")  # Логируем входящие данные
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://your-server.com/{TOKEN}")
    return "Webhook set!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
