from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import logging

# Токен бота (замени на свой)
TOKEN = "8118288915:AAFetk_yAXr517sDSuG6NZ2yFi96q-ETvoU"
ORGANIZER_ID = "Y318677172"  # Куда будут приходить ответы гостей

# File IDs фотографий (замени на свои)
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

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, "Привет! Добро пожаловать на нашу свадьбу! 🎉")
    
    for photo in PHOTO_IDS[:3]:
        context.bot.send_photo(chat_id, photo)
    
    context.bot.send_message(chat_id, "📍 Локация: Forest Glamp [Ссылка](https://2gis.ru/ufa/geo/70000001081557905/55.265181,55.122961) (предусмотрены домики для ночевки 🛏)\n\n🚌 Трансфер - 13:30, длительность 1 час 40 минут. Обратно в 11:30\n\n⏳ Тайминг:\n- 15:30 Фуршет\n- 16:00 Церемония\n- 16:40 Банкет\n- 23:00 Завершение", parse_mode='Markdown')
    
    for photo in PHOTO_IDS[3:]:
        context.bot.send_photo(chat_id, photo)
    
    # Запуск опроса
    ask_attendance(update, context)

def ask_attendance(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Да", callback_data='attending_yes'),
                 InlineKeyboardButton("Нет", callback_data='attending_no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ты придёшь на свадьбу?", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    response = query.data
    
    # Отправка организатору
    context.bot.send_message(ORGANIZER_ID, f"Ответ от {query.message.chat.first_name}: {response}")
    
    steps = {
        'attending_yes': ("Будешь с +1?", ['plus_one_yes', 'plus_one_no']),
        'plus_one_yes': ("Остаёшься с ночёвкой?", ['stay_yes', 'stay_no']),
        'plus_one_no': ("Остаёшься с ночёвкой?", ['stay_yes', 'stay_no']),
        'stay_yes': ("Тебе нужен трансфер?", ['transfer_both', 'transfer_to', 'transfer_from', 'transfer_no']),
        'stay_no': ("Тебе нужен трансфер?", ['transfer_both', 'transfer_to', 'transfer_from', 'transfer_no']),
        'transfer_both': ("Какое меню выберешь?", ['menu_meat', 'menu_fish']),
        'transfer_to': ("Какое меню выберешь?", ['menu_meat', 'menu_fish']),
        'transfer_from': ("Какое меню выберешь?", ['menu_meat', 'menu_fish']),
        'transfer_no': ("Какое меню выберешь?", ['menu_meat', 'menu_fish']),
        'menu_meat': ("Выбери напитки (можно несколько):", ['drink_champagne', 'drink_redwine', 'drink_whitewine', 'drink_martini', 'drink_strong', 'drink_nonalc']),
        'menu_fish': ("Выбери напитки (можно несколько):", ['drink_champagne', 'drink_redwine', 'drink_whitewine', 'drink_martini', 'drink_strong', 'drink_nonalc'])
    }
    
    if response in steps:
        text, options = steps[response]
        buttons = [[InlineKeyboardButton(option.replace('_', ' '), callback_data=option)] for option in options]
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        query.edit_message_text("Спасибо за участие! Если допустили ошибку, нажмите /start и пройдите опрос заново. Ссылка на свадебный чат: [Перейти](https://t.me/+YnMBjkthhZ1mN2Qy)", parse_mode='Markdown')

def notify_guests(update: Update, context: CallbackContext):
    if str(update.message.chat_id) == ORGANIZER_ID:
        message = update.message.text.replace("/notify ", "")
        for guest in context.bot_data.get("guests", []):
            context.bot.send_message(guest, f"📢 Важное сообщение от организатора:\n{message}")
        update.message.reply_text("Сообщение отправлено всем гостям.")
    else:
        update.message.reply_text("Эта команда только для организатора.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("notify", notify_guests))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
