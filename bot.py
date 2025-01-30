import logging
from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = "8118288915:AAFetk_yAXr517sDSuG6NZ2yFi96q-ETvoU"

# ID организатора
ORGANIZER_ID = 318677172

# ID фото
PHOTO_IDS = [
    "AAMCAgADGQEBxq37Z5ud5B6CXi7slU3qf_Mzj1lvcnsAAghuAAJUTuBIigTVuYm2AzABAAdtAAM2BA",
    "AAMCAgADGQEBxq5TZ5ue3HZk18lBvi-f8PbtMKFRwzYAAiluAAJUTuBIegOfV6nETpoBAAdtAAM2BA",
    "AAMCAgADGQEBxq5oZ5ue6n7KvKI8a651oCVfjw2BEXgAAixuAAJUTuBINxAc6s1cR2oBAAdtAAM2BA",
    "AAMCAgADGQEBxq54Z5ufEvMrro6Fz5HWbr6mXqj4x1IAAjFuAAJUTuBIxFuQG_5YdKoBAAdtAAM2BA",
    "AAMCAgADGQEBxq57Z5ufGBrMKydlrY7XDlABXD4EheYAAjJuAAJUTuBIOBsc5sJj64wBAAdtAAM2BA",
    "AAMCAgADGQEBxq6KZ5ufPaicgL3RRnzbwGESoqPWz54AAjtuAAJUTuBIBOx-bjDTcrYBAAdtAAM2BA",
    "AAMCAgADGQEBxq6OZ5ufUJ2AlIaCymTFE47SzUHiusMAAkBuAAJUTuBInQHldAOFVOsBAAdtAAM2BA",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Отправляем фото
    for photo_id in PHOTO_IDS[:3]:
        await context.bot.send_photo(chat_id=user_id, photo=photo_id)

    # Отправляем информацию о свадьбе
    info_text = (
        "📍Локация: Forest Glamp https://2gis.ru/ufa/geo/70000001081557905/55.265181,55.122961 (предусмотрены домики для ночевки🛏 )\n\n"
        "🚌 Трансфер - Предварительное время 13:30, длительность 1 час 40 минут. Обратно на следующий день к 11:30\n"
        "⏳ Тайминг свадьбы - 15:30 - Фуршет, 16:00 - Свадебная церемония, 16:40 - Банкет, 23:00 - Завершение торжества"
    )
    await update.message.reply_text(info_text)

    # Отправляем оставшиеся фото
    for photo_id in PHOTO_IDS[3:]:
        await context.bot.send_photo(chat_id=user_id, photo=photo_id)

    # Запускаем опрос
    await start_poll(update, context)

async def start_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["responses"] = {}
    await poll_1(update, context)

# Вопросы для опроса
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

# Обработчик сообщений
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
        if isinstance(answer, list):  # Если ответ на poll_6 - список
            message += f"{question}: {', '.join(answer)}\n"
        else:
            message += f"{question}: {answer}\n"

    await context.bot.send_message(chat_id=ORGANIZER_ID, text=message)
    await update.message.reply_text("Спасибо за участие!\n\nЕсли допустили ошибку – просто нажмите /start и пройдите опрос заново. Ссылка на свадебный чат для обмена информации и фотографий https://t.me/+YnMBjkthhZ1mN2Qy")

# ... (остальной код остается без изменений)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Этот бот поможет вам получить информацию о свадьбе и ответить на вопросы.")

#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("Привет! Этот бот поможет вам получить информацию о свадьбе и ответить на вопросы. Нажмите /start для начала.")

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

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Запуск бота
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Добавляем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
