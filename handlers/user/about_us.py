from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp


@dp.message_handler(F.text == "🍪 Biz haqimizda")
async def handle_about_us(message: types.Message, state: FSMContext):
    await state.finish()
    about_text = (
        "Matn yozish kerak"
    )
    await message.answer(about_text)
