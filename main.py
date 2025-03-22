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
API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("Токен бота не найден в файле .env. Укажи BOT_TOKEN в .env!")

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
        "Приветствую, кожаный. \nЯ бот для изучения мата на трёх языках.\n\n"
        "Используй команды:\n"
        "/russian — случайный русский мат\n"
        "/english — случайный английский мат\n"
        "/spanish — случайный испанский мат\n\n"
        "Транскрипция поможет тебе правильно произнести слова!"
    )

# Обработчик команды /russian
@dp.message(Command("russian"))
async def random_russian_swear(message: Message):
    swear = random.choice(data["swear_words"]["russian"])
    word = swear["word"]
    transcription = swear["transcription"]
    eng_trans = swear["translations"]["english"]["word"]
    eng_transcription = swear["translations"]["english"]["transcription"]
    spa_trans = swear["translations"]["spanish"]["word"]
    spa_transcription = swear["translations"]["spanish"]["transcription"]
    
    response = (
        f"⚪ {word} ({transcription})\n"
        f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 {eng_trans} ({eng_transcription})\n"
        f"🇪🇸 {spa_trans} ({spa_transcription})"
    )
    await message.reply(response)

# Обработчик команды /english
@dp.message(Command("english"))
async def random_english_swear(message: Message):
    swear = random.choice(data["swear_words"]["english"])
    word = swear["word"]
    transcription = swear["transcription"]
    rus_trans = swear["translations"]["russian"]["word"]
    rus_transcription = swear["translations"]["russian"]["transcription"]
    spa_trans = swear["translations"]["spanish"]["word"]
    spa_transcription = swear["translations"]["spanish"]["transcription"]
    
    response = (
        f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 {word} ({transcription})\n"
        f"⚪ {rus_trans} ({rus_transcription})\n"
        f"🇪🇸 {spa_trans} ({spa_transcription})"
    )
    await message.reply(response)

# Обработчик команды /spanish
@dp.message(Command("spanish"))
async def random_spanish_swear(message: Message):
    swear = random.choice(data["swear_words"]["spanish"])
    word = swear["word"]
    transcription = swear["transcription"]
    rus_trans = swear["translations"]["russian"]["word"]
    rus_transcription = swear["translations"]["russian"]["transcription"]
    eng_trans = swear["translations"]["english"]["word"]
    eng_transcription = swear["translations"]["english"]["transcription"]
    
    response = (
        f"🇪🇸 {word} ({transcription})\n"
        f"⚪ {rus_trans} ({rus_transcription})\n"
        f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 {eng_trans} ({eng_transcription})"
    )
    await message.reply(response)

# Запуск бота
async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())