import json, datetime
from aiogram import Router, types, Bot
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from ..database import SessionLocal
from ..models import UserProgress
from ..tts import get_audio

router = Router()

LESSONS = json.load(open("data/lessons.json", encoding="utf8"))
FIRST_BATCH = 5
EXTRA_BATCH = 2

def get_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Получить слова", callback_data="get_words")],
        [InlineKeyboardButton(text="🔁 Повторить прошлые слова", callback_data="repeat")],
        [InlineKeyboardButton(text="📈 Мой прогресс", callback_data="progress")],
        [InlineKeyboardButton(text="➕ Хочу ещё", callback_data="more")]
    ])

async def send_words(uid: int, bot: Bot, is_first=False, repeat=False):
    async with SessionLocal() as db:
        rec = await db.get(UserProgress, uid)
        if not rec:
            rec = UserProgress(user_id=uid, last_index=0)
            db.add(rec)

        today = datetime.date.today()
        if rec.last_sent != today:
            rec.last_sent = today
            await db.commit()

        batch_size = FIRST_BATCH if is_first else EXTRA_BATCH

        if repeat:
            start = max(0, rec.last_index - batch_size)
        else:
            start = rec.last_index

        chunk = LESSONS[start:start + batch_size]
        if not chunk:
            await bot.send_message(uid, "Слова закончились, приходи завтра 😊", reply_markup=get_buttons())
            return

        texts = []
        for it in chunk:
            word = it["en"]
            ru = it["ru"]
            ex = it["example"]
            ex_ru = it["example_ru"]
            texts.append(f"{word} — {ru}\n{ex}\n{ex_ru}")

            audio_word = await get_audio(f"{word}.mp3", word)
            await bot.send_audio(uid, FSInputFile(audio_word))

            audio_example = await get_audio(f"{word}_ex.mp3", ex)
            await bot.send_audio(uid, FSInputFile(audio_example))

        if not repeat:
            rec.last_index += len(chunk)  # обновляем точно на длину, а не batch_size
            await db.commit()

        await bot.send_message(uid, "\n\n".join(texts), reply_markup=get_buttons())

@router.callback_query(lambda c: c.data == "get_words")
async def get_words_callback(call: types.CallbackQuery):
    await send_words(call.from_user.id, call.bot, is_first=True)
    await call.answer()

@router.callback_query(lambda c: c.data == "more")
async def more_callback(call: types.CallbackQuery):
    await send_words(call.from_user.id, call.bot)
    await call.answer()

@router.callback_query(lambda c: c.data == "repeat")
async def repeat_callback(call: types.CallbackQuery):
    await send_words(call.from_user.id, call.bot, repeat=True)
    await call.answer("Повторяем прошлые слова")

@router.callback_query(lambda c: c.data == "progress")
async def progress_callback(call: types.CallbackQuery):
    async with SessionLocal() as db:
        rec = await db.get(UserProgress, call.from_user.id)
        if rec:
            total = len(LESSONS)
            learned = rec.last_index or 0
            percent = int(learned / total * 100) if total else 0
            recent_words = LESSONS[max(0, learned - 3):learned]

            lines = [f"📊 Ты выучил {learned} из {total} слов ({percent}%)"]
            if recent_words:
                lines.append("\n🧠 Последние слова:")
                for item in recent_words:
                    lines.append(f"• {item['en']} — {item['ru']}")
            await call.message.answer("\n".join(lines), reply_markup=get_buttons())
        else:
            await call.message.answer("Пока нет прогресса — начни учиться!", reply_markup=get_buttons())
    await call.answer()
