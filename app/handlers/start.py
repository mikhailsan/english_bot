from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.handlers.words import send_words

router = Router()

@router.message(lambda m: m.text and ("старт" in m.text.lower() or "start" in m.text.lower()))
async def start_handler(msg: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Получить слова", callback_data="get_words")],
        [InlineKeyboardButton(text="🔁 Повторить прошлые слова", callback_data="repeat_words")],
        [InlineKeyboardButton(text="📈 Мой прогресс", callback_data="my_progress")]
    ])
    await msg.answer(
        "👋 Привет! Я помогу тебе учить английские слова каждый день.\n\nВыбери, что хочешь сделать:",
        reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data == "get_words")
async def get_words(call: types.CallbackQuery):
    await send_words(call.from_user.id, call.bot, is_first=True)
    await call.answer()

@router.callback_query(lambda c: c.data == "repeat_words")
async def repeat_words(call: types.CallbackQuery):
    await call.message.answer("🔁 Повторение прошлых слов пока не реализовано. Но скоро будет!")
    await call.answer()

@router.callback_query(lambda c: c.data == "my_progress")
async def my_progress(call: types.CallbackQuery):
    await call.message.answer("📈 Отображение прогресса пока не реализовано. Но мы уже работаем над этим!")
    await call.answer()
