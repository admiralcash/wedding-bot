import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from flask import Flask
from threading import Thread

# --- Настройки бота ---
TOKEN = "8118288915:AAFetk_yAXr517sDSuG6NZ2yFi96q-ETvoU"
ADMIN_ID = 318677172  # ЗАМЕНИ НА СВОЙ ID (узнать можно в @userinfobot)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Веб-сервер для UptimeRobot ---
app = Flask(__name__)


@app.route('/')
def home():
    return "Бот работает!"


def run():
    app.run(host="0.0.0.0", port=8080, debug=False)


def keep_alive():
    print("Запускаем веб-сервер Flask...")
    server = Thread(target=run)
    server.daemon = True
    server.start()


# --- Определяем шаги опроса ---
class Survey(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()


# --- Приветственное сообщение ---
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    print(f"Бот получил /start от {message.from_user.id}")  # Лог в консоль
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Начать опрос")]], resize_keyboard=True)
    await message.answer(
        "Привет! Ты получил приглашение на свадьбу! 🎉 Давай ответим на несколько вопросов.",
        reply_markup=keyboard)


# --- Начало опроса ---
@dp.message(F.text == "Начать опрос")
async def start_poll(message: types.Message, state: FSMContext):
    print(f"Бот получил 'Начать опрос' от {message.from_user.id}")  # Лог
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да")],
                                             [KeyboardButton(text="Нет")]],
                                   resize_keyboard=True)
    await state.set_state(Survey.q1)
    await message.answer("Ты придёшь на свадьбу?", reply_markup=keyboard)


# --- Вопрос 2: Будешь с +1? ---
@dp.message(Survey.q1, F.text.in_(["Да", "Нет"]))
async def answer_q1(message: types.Message, state: FSMContext):
    await state.update_data(q1=message.text)
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да")],
                                             [KeyboardButton(text="Нет")]],
                                   resize_keyboard=True)
    await state.set_state(Survey.q2)
    await message.answer("Ты будешь с +1?", reply_markup=keyboard)


# --- Вопрос 3: Нужен ли трансфер? ---
@dp.message(Survey.q2, F.text.in_(["Да", "Нет"]))
async def answer_q2(message: types.Message, state: FSMContext):
    await state.update_data(q2=message.text)
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да")],
                                             [KeyboardButton(text="Нет")]],
                                   resize_keyboard=True)
    await state.set_state(Survey.q3)
    await message.answer("Тебе нужен трансфер?", reply_markup=keyboard)


# --- Вопрос 4: Какое меню выберешь? ---
@dp.message(Survey.q3, F.text.in_(["Да", "Нет"]))
async def answer_q3(message: types.Message, state: FSMContext):
    await state.update_data(q3=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Мясное")],
                  [KeyboardButton(text="Рыбное")],
                  [KeyboardButton(text="Вегетарианское")]],
        resize_keyboard=True)
    await state.set_state(Survey.q4)
    await message.answer("Какое меню выберешь?", reply_markup=keyboard)


# --- Завершаем опрос и отправляем ответы админу ---
@dp.message(Survey.q4, F.text.in_(["Мясное", "Рыбное", "Вегетарианское"]))
async def answer_q4(message: types.Message, state: FSMContext):
    await state.update_data(q4=message.text)
    data = await state.get_data()
    await state.clear()

    # Формируем текст с ответами
    result_text = (
        f"📝 Новый ответ от {message.from_user.full_name} (@{message.from_user.username}):\n"
        f"1️⃣ Придёт на свадьбу: {data['q1']}\n"
        f"2️⃣ С +1: {data['q2']}\n"
        f"3️⃣ Нужен трансфер: {data['q3']}\n"
        f"4️⃣ Меню: {data['q4']}")

    # Отправляем ответ пользователю
    await message.answer("Спасибо! Ответы отправлены организатору. 🎉")

    # Отправляем организатору
    await bot.send_message(ADMIN_ID, result_text)


# --- Запуск бота ---
async def start_bot():
    print("Бот запущен...")
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f"Ошибка polling: {e}")
            await asyncio.sleep(5)  # Перезапуск через 5 секунд


if __name__ == "__main__":
    keep_alive()  # Запускаем веб-сервер перед ботом
    asyncio.run(start_bot())
