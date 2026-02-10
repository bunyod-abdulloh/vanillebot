from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.inline.user.base_ikbs import feedback_ikb
from loader import dp, bot


@dp.message_handler(F.text == "💬 Taklif va shikoyatlar", state="*")
async def handle_feedbacks(message: types.Message, state: FSMContext):
    await message.answer("Taklif va shikoyatlaringizni yozib qoldiring. Biz ularni ko'rib chiqamiz va imkon qadar "
                         "tezroq javob beramiz.")

    await state.set_state("awaiting_feedback")


@dp.message_handler(state="awaiting_feedback", content_types=types.ContentTypes.TEXT)
async def receive_feedback(message: types.Message, state: FSMContext):
    feedback = message.text

    full_name = message.from_user.full_name
    telegram_id = int(message.from_user.id)

    await bot.send_message(
        chat_id=ADMINS[0],
        text=f"Yangi taklif/shikoyat:\n\n{feedback}\n\n"
             f"Yuboruvchi: {full_name}",
        reply_markup=feedback_ikb(telegram_id)
    )
    await message.answer("Taklif va shikoyatingiz uchun rahmat! Biz uni ko'rib chiqamiz.")

    await state.finish()
