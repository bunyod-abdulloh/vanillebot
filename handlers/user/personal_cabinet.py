from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.user.base_ikbs import edit_datas_ikb
from loader import dp, udb


@dp.message_handler(F.text == "🧁 Shaxsiy kabinet", state="*")
async def personal_kabinet(message: types.Message, state: FSMContext):
    await state.finish()

    telegram_id = int(message.from_user.id)

    user = await udb.get_user(telegram_id)

    if user:
        full_name = user['full_name']
        phone_number = user['phone_number'] if user['phone_number'] else "N/A"

        response_text = f"👤 Shaxsiy kabinet\n\nIsm: {full_name}\nTelefon raqam: {phone_number}"
        await message.answer(text=response_text, reply_markup=edit_datas_ikb())
