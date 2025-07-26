import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Инициализация базы данных и планировщика
from app.database import init_db
from app.scheduler import setup as sched_setup

# Импорт роутеров
from app.handlers import start, words

# Загружаем токен из .env
load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))

# Создаём диспетчер и подключаем роутеры
dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(words.router)

async def main():
    await init_db()         # Инициализация БД
    sched_setup(bot)        # Настройка планировщика (если используется)
    await dp.start_polling(bot)  # Запуск бота

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
