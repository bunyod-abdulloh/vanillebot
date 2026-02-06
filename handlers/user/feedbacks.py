from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from loader import dp, bot, udb


@dp.message_handler(F.text == "💬 Taklif va shikoyatlar", state="*")
async def handle_feedbacks(message: types.Message, state: FSMContext):
    await message.answer("Taklif va shikoyatlaringizni yozib qoldiring. Biz ularni ko'rib chiqamiz va imkon qadar "
                         "tezroq javob beramiz.")

    await state.set_state("awaiting_feedback")


@dp.message_handler(state="awaiting_feedback", content_types=types.ContentTypes.TEXT)
async def receive_feedback(message: types.Message, state: FSMContext):
    feedback = message.text
    telegram_id = int(message.from_user.id)

    user = await udb.get_user(telegram_id)

    if user:
        full_name = user["full_name"]
        phone_number = user["phone_number"]

        await bot.send_message(
            chat_id=ADMINS[0],
            text=f"Yangi taklif/shikoyat:\n\n{feedback}\n\n"
                 f"Yuboruvchi: {full_name}\nTelefon raqam: {phone_number}"
        )
        await message.answer("Taklif va shikoyatingiz uchun rahmat! Biz uni ko'rib chiqamiz.")

        await state.finish()
    else:
        await message.answer(
            "Siz tizimda ro'yxatdan o'tmagansiz. Iltimos, /start buyrug'ini kiritib avval ro'yxatdan o'ting."
        )
        await state.finish()
