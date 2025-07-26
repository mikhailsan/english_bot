import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import SessionLocal
from app.models import UserProgress
from app.handlers.words import send_words
from aiogram import Bot, types

def setup(bot: Bot):
    scheduler = AsyncIOScheduler()

    @scheduler.scheduled_job("cron", hour=10, minute=0)  # ⏰ Каждый день в 10:00
    async def job():
        async with SessionLocal() as db:
            today = datetime.date.today()
            users = await db.execute(
                db.select(UserProgress)
            )
            users = users.scalars().all()

            for user in users:
                if user.last_sent != today:
                    try:
                        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                            [types.InlineKeyboardButton(text="📚 Получить слова", callback_data="more")]
                        ])
                        await bot.send_message(
                            user.user_id,
                            "👋 Привет! Не забудь получить свои английские слова на сегодня!\nНажми кнопку ниже 👇",
                            reply_markup=keyboard
                        )
                    except Exception as e:
                        print(f"❌ Не удалось отправить сообщение пользователю {user.user_id}: {e}")

    scheduler.start()

