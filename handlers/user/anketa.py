from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.user.user_buttons import get_phone_dkb, user_main_button
from loader import dp, udb
from services.helper_functions import validate_full_name, validate_phone_number


@dp.message_handler(state="get_full_name")
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text.strip()

    if not validate_full_name(full_name):
        await message.answer(
            "Iltimos, ism va familiyangizni lotincha, bitta probel bilan kiriting"
        )
        return

    await state.update_data(user_fullname=full_name)

    await message.answer(
        text="Telefon raqamingizni kiriting\n\nFormat: +998XXXXXXXXX\n\nYoki pastdagi tugmani bosing va kontaktni "
             "yuboring.", reply_markup=get_phone_dkb()
    )
    await state.set_state("get_phone_number")


@dp.message_handler(state="get_phone_number", content_types=["text", "contact"])
async def get_phone_number(message: types.Message, state: FSMContext):
    if message.content_type == "contact":
        phone_number = message.contact.phone_number
        if phone_number.startswith("998"):
            phone_number = "+" + phone_number
    else:
        phone_number = message.text.strip()

    if not validate_phone_number(phone_number):
        await message.answer("Iltimos, telefon raqamingizni +998XXXXXXXXX formatida kiriting!")
        return

    user_data = await state.get_data()
    full_name = user_data.get("user_fullname")

    await udb.add_user(
        telegram_id=int(message.from_user.id),
        full_name=full_name,
        phone_number=phone_number
    )

    await message.answer(
        text=f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\nIsm sharifingiz: {full_name}\n"
             f"Telefon raqamingiz: {phone_number}",
        reply_markup=user_main_button()
    )
    await state.finish()
