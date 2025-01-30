import logging
import threading
from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    PicklePersistence,
)
from flask import Flask, request

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = "8118288915:AAFetk_yAXр517sDSuG6NZ2yFi96q-ETvoU"

# ID организатора
ORGANIZER_ID = 318677172

# ID фото
PHOTO_IDS = [
    "AAMCAgADGQEBxq37Z5ud5B6CXi7slU3qf_Mzj1lvcnsAAghuAAJUTuBIigTVuYm2AzABAAdtAAM2BA",  # 1
    "AAMCAgADGQEBxq5TZ5ue3HZk18lBvi-f8PbtMKFRwzYAAiluAAJUTuBIegOfV6nETpoBAAdtAAM2BA",  # 2
    "AAMCAgADGQEBxq5oZ5ue6n7KvKI8a651oCVfjw2BEXgAAixuAAJUTuBINxAc6s1cR2oBAAdtAAM2BA",  # 3
    "AAMCAgADGQEBxq54Z5ufEvMrro6Fz5HWbr6mXqj4x1IAAjFuAAJUTuBIxFuQG_5YdKoBAAdtAAM2BA",  # 4
    "AAMCAgADGQEBxq57Z5ufGBrMKydlrY7XDlABXD4EheYAAjJuAAJUTuBIOBsc5sJj64wBAAdtAAM2BA",  # 5
    "AAMCAgADGQEBxq6KZ5ufPaicgL3RRnzbwGESoqPWz54AAjtuAAJUTuBIBOx-bjDTcrYBAAdtAAM2BA",  # 6
    "AAMCAgADGQEBxq6OZ5ufUJ2AlIaCymTFE47SzUHiusMAAkBuAAJUTuBInQHldAOFVOsBAAdtAAM2BA",  # 7
]

app = Flask(__name__)

# --- Опрос ---
async def start_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["responses"] = {}
    await poll_1(update, context)

async def poll_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Ты придёшь на свадьбу?"
    keyboard = ReplyKeyboardMarkup([["Да", "Нет"]], resize_keyboard=True)
    await update.message.reply_text(question, reply_markup=keyboard)
    context.chat_data["current_poll"] = "poll_1"

async def poll_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Будешь с +1?"
    keyboard = ReplyKeyboardMarkup([["Да", "Нет"]], resize_keyboard=True)
    await update.message.reply_text(question, reply_markup=keyboard)
    context.chat_data["current_poll"] = "poll_2"

async def poll_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Остаешься ли с ночевкой?"
    keyboard = ReplyKeyboardMarkup([["Да", "Нет"]], resize_keyboard=True)
    await update.message.reply_text(question, reply_markup=keyboard)
    context.chat_data["current_poll"] = "poll_3"

async def poll_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Тебе нужен трансфер?"
    keyboard = ReplyKeyboardMarkup([["Да, в обе стороны", "Только на свадьбу", "Только со свадьбы", "Нет, приеду на машине"]], resize_keyboard=True)
    await update.message.reply_text(question, reply_markup=keyboard)
    context.chat_data["current_poll"] = "poll_4"

async def poll_5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Какое меню выберешь?"
    keyboard = ReplyKeyboardMarkup([["Мясо", "Рыба"]], resize_keyboard=True)
    await update.message.reply_text(question, reply_markup=keyboard)
    context.chat_data["current_poll"] = "poll_5"

async def poll_6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Выбор напитков (можно выбрать несколько):"
    keyboard = ReplyKeyboardMarkup([["Шампанское", "Красное вино", "Белое вино"], ["Мартини", "Крепкий алкоголь", "Безалкогольные напитки"]], resize_keyboard=True)
    await update.message.reply_text(question, reply_markup=keyboard)
    context.chat_data["current_poll"] = "poll_6"

async def poll_7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Какие есть пожелания/вопросы?"
    await update.message.reply_text(question, reply_markup=ForceReply(selective=True))
    context.chat_data["current_poll"] = "poll_7"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text
    current_poll = context.chat_data.get("current_poll")
    responses = context.chat_data.get("responses")

    if current_poll:
        if current_poll == "poll_6":
            if current_poll not in responses:
                context.chat_data["responses"][current_poll] = [message_text]
            else:
                context.chat_data["responses"][current_poll].append(message_text)
        else:
            context.chat_data["responses"][current_poll] = message_text
        await update.message.reply_text("Спасибо за ответ!")

        if current_poll == "poll_1":
            await poll_2(update, context)
        elif current_poll == "poll_2":
            await poll_3(update, context)
        elif current_poll == "poll_3":
            await poll_4(update, context)
        elif current_poll == "poll_4":
            await poll_5(update, context)
        elif current_poll == "poll_5":
            await poll_6(update, context)
        elif current_poll == "poll_6":
            await poll_7(update, context)
        elif current_poll == "poll_7":
            await finish_poll(update, context)

async def finish_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responses = context.chat_data["responses"]
    message = "Ответы на опрос:\n"
    for question, answer in responses.items():
        if isinstance(answer, list):
            message += f"{question}: {', '.join(answer)}\n"
        else:
            message += f"{question}: {answer}\n"

    await context.bot.send_message(chat_id=ORGANIZER_ID, text=message)
    await update.message.reply_text("Спасибо за участие!\n\nЕсли допустили ошибку – просто нажмите /start и пройдите опрос заново. Ссылка на свадебный чат для обмена информации и фотографий https://t.me/+YnMBjkthhZ1mN2Qy")
# --- Конец опроса ---


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    context.bot_data["all_users"] = context.bot_data.get("all_users", [])
    context.bot_data["all_users"].append(user_id)

    # Отправляем фото (3 фото)
    for photo_id in PHOTO_IDS[:3]:
        await context.bot.send_photo(chat_id=user_id, photo=photo_id)

    # Отправляем информацию о свадьбе
    info_text = (
        "📍Локация: Forest Glamp https://2gis.ru/ufa/geo/70000001081557905/55.265181,55.122961 (предусмотрены домики для ночевки🛏 )\n\n"
        "🚌 Трансфер - Предварительное время 13:30, длительность 1 час 40 минут. Обратно на следующий день к 11:30\n"
        "⏳ Тайминг свадьбы - 15:30 - Фуршет, 16:00 - Свадебная церемония, 16:40 - Банкет, 23:00 - Завершение торжества"
    )
    await update.message.reply_text(info_text)

    # Отправляем оставшиеся фото (4 фото)
    for photo_id in PHOTO_IDS[3:]:
        await context.bot.send_photo(chat_id=user_id, photo=photo_id)

    # Запускаем опрос
    await start_poll(update, context)


# Функция для отправки уведомлений
async def send_notification(context: ContextTypes.DEFAULT_TYPE, message: str):
    for user_id in context.bot_data["all_users"]:  # Используем список всех пользователей из bot_data
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logging.error(f"Ошибка отправки уведомления пользователю {user_id}: {e}")

async def notify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ORGANIZER_ID:
        message = update.message.text.replace("/notify ", "")
        await send_notification(context, message)

# --- Flask ---
def run_telegram_bot():
    persistence = PicklePersistence(filepath="bot_data")  # Используем PicklePersistence для сохранения данных
    application = ApplicationBuilder().token(BOT_TOKEN).persistence(persistence).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("notify", notify_command))
    application.run_polling()

telegram_thread = threading.Thread(target=run_telegram_bot)
telegram_thread.daemon = True
telegram_thread.start()

@app.route('/', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return 'ok'

@app.route('/', methods=['GET'])
def index():
    return "Telegram bot is running!"

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    # app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # для локального запуска
    app.run(host='0.0.0.0', port=5000)  # Timeweb будет использовать этот порт
