import asyncio
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from dotenv import load_dotenv
import os

# Загрузка переменных из .env
load_dotenv()

# Получение токена из переменной окружения
API_TOKEN = os.getenv("BOT_TOKEN")

# Проверка, что токен загружен
if not API_TOKEN:
    raise ValueError("Токен бота не найден в файле .env. Укажи BOT_TOKEN в .env!")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Загрузка JSON-файла с ругательствами
with open('swear_words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Функция для установки команд в меню
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/russian", description="Случайный русский мат"),
        BotCommand(command="/english", description="Случайный английский мат"),
        BotCommand(command="/spanish", description="Случайный испанский мат")
    ]
    await bot.set_my_commands(commands)

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply(
        "Привет! Я бот для изучения мата на трёх языках.\n"
        "Используй команды:\n"
        "/russian — случайный русский мат\n"
        "/english — случайный английский мат\n"
        "/spanish — случайный испанский мат"
    )

# Обработчик команды /russian
@dp.message(Command("russian"))
async def random_russian_swear(message: Message):
    swear = random.choice(data["swear_words"]["russian"])
    word = swear["word"]
    eng_trans = swear["translations"]["english"]
    spa_trans = swear["translations"]["spanish"]
    response = f"{word} (🏴󠁧󠁢󠁥󠁮󠁧󠁿{eng_trans}, 🇪🇸{spa_trans})"
    await message.reply(response)

# Обработчик команды /english
@dp.message(Command("english"))
async def random_english_swear(message: Message):
    swear = random.choice(data["swear_words"]["english"])
    word = swear["word"]
    rus_trans = swear["translations"]["russian"]
    spa_trans = swear["translations"]["spanish"]
    response = f"🏴󠁧󠁢󠁥󠁮󠁧󠁿{word} ({rus_trans}, 🇪🇸{spa_trans})"
    await message.reply(response)

# Обработчик команды /spanish
@dp.message(Command("spanish"))
async def random_spanish_swear(message: Message):
    swear = random.choice(data["swear_words"]["spanish"])
    word = swear["word"]
    rus_trans = swear["translations"]["russian"]
    eng_trans = swear["translations"]["english"]
    response = f"🇪🇸{word} ({rus_trans}, 🏴󠁧󠁢󠁥󠁮󠁧󠁿{eng_trans})"
    await message.reply(response)

# Запуск бота
async def main():
    # Установка команд в меню при запуске
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())