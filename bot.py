from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging

# Токен бота и ID организатора
TOKEN = "8118288915:AAFetk_yAXr517sDSuG6NZ2yFi96q-ETvoU"
ORGANIZER_ID = "318677172"

# File IDs фотографий
PHOTO_IDS = [
    "AAMCAgADGQEBxq37Z5ud5B6CXi7slU3qf_Mzj1lvcnsAAghuAAJUTuBIigTVuYm2AzABAAdtAAM2BA", 
    "AAMCAgADGQEBxq5TZ5ue3HZk18lBvi-f8PbtMKFRwzYAAiluAAJUTuBIegOfV6nETpoBAAdtAAM2BA", 
    "AAMCAgADGQEBxq5oZ5ue6n7KvKI8a651oCVfjw2BEXgAAixuAAJUTuBINxAc6s1cR2oBAAdtAAM2BA", 
    "AAMCAgADGQEBxq54Z5ufEvMrro6Fz5HWbr6mXqj4x1IAAjFuAAJUTuBIxFuQG_5YdKoBAAdtAAM2BA", 
    "AAMCAgADGQEBxq57Z5ufGBrMKydlrY7XDlABXD4EheYAAjJuAAJUTuBIOBsc5sJj64wBAAdtAAM2BA", 
    "AAMCAgADGQEBxq6KZ5ufPaicgL3RRnzbwGESoqPWz54AAjtuAAJUTuBIBOx-bjDTcrYBAAdtAAM2BA", 
    "AAMCAgADGQEBxq6OZ5ufUJ2AlIaCymTFE47SzUHiusMAAkBuAAJUTuBInQHldAOFVOsBAAdtAAM2BA"
]

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, "Привет! Добро пожаловать на нашу свадьбу! 🎉")
    
    for photo in PHOTO_IDS[:3]:
        context.bot.send_photo(chat_id, photo)
    
    context.bot.send_message(chat_id, "📍 Локация: Forest Glamp [Ссылка](https://2gis.ru/ufa/geo/70000001081557905/55.265181,55.122961) (предусмотрены домики для ночевки 🛏)\n\n🚌 Трансфер - 13:30, длительность 1 час 40 минут. Обратно в 11:30\n\n⏳ Тайминг:\n- 15:30 Фуршет\n- 16:00 Церемония\n- 16:40 Банкет\n- 23:00 Завершение", parse_mode='Markdown')
    
    for photo in PHOTO_IDS[3:]:
        context.bot.send_photo(chat_id, photo)
    
    ask_attendance(update, context)

def ask_attendance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Да", callback_data='attending_yes'),
                 InlineKeyboardButton("Нет", callback_data='attending_no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ты придёшь на свадьбу?", reply_markup=reply_markup)

def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    response = query.data
    context.bot.send_message(ORGANIZER_ID, f"Ответ от {query.message.chat.first_name}: {response}")
    
    next_questions = {
        'attending_yes': "Будешь с +1?",
        'plus_one_yes': "Остаёшься с ночёвкой?",
        'stay_yes': "Тебе нужен трансфер?",
        'transfer_both': "Какое меню выберешь?",
        'menu_meat': "Выбери напитки (можно несколько):",
        'menu_fish': "Выбери напитки (можно несколько):"
    }
    
    if response in next_questions:
        query.edit_message_text(next_questions[response], reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Да", callback_data=response + '_yes'), InlineKeyboardButton("Нет", callback_data=response + '_no')]
        ]))
    else:
        query.edit_message_text("Спасибо за участие! Если допустили ошибку, нажмите /start и пройдите опрос заново. Ссылка на свадебный чат: [Перейти](https://t.me/+YnMBjkthhZ1mN2Qy)", parse_mode='Markdown')

def notify_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.chat_id) == ORGANIZER_ID:
        message = update.message.text.replace("/notify ", "")
        update.message.reply_text("Сообщение отправлено всем гостям.")
    else:
        update.message.reply_text("Эта команда только для организатора.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("notify", notify_guests))
    application.run_polling()

if __name__ == "__main__":
    main()
