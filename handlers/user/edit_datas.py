from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.default.user.user_buttons import get_location_dkb, user_main_button
from loader import dp, clsdb
from services.helper_functions import validate_full_name, validate_phone_number


@dp.callback_query_handler(F.data == "edit_name", state="*")
async def edit_full_name(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    text = "Yangi ism - familiyangizni kiriting:"
    await call.message.edit_text(text)
    await state.set_state("edit_full_name")


@dp.message_handler(state="edit_full_name")
async def process_full_name(message: types.Message, state: FSMContext):
    full_name = message.text.strip()

    if not validate_full_name(full_name):
        await message.answer(
            "Iltimos, ism va familiyangizni lotincha, bitta probel bilan kiriting"
        )
        return

    telegram_id = int(message.from_user.id)

    await clsdb.set_full_name(full_name, telegram_id)

    await message.answer(
        text="Ism - familiyangiz muvaffaqiyatli o'zgartirildi!"
    )
    await state.finish()


@dp.callback_query_handler(F.data == "edit_phone", state="*")
async def edit_phone_number(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    text = "Yangi telefon raqamingizni kiriting:\n\nFormat: +998XXXXXXXXX"
    await call.message.edit_text(text)
    await state.set_state("edit_phone_number")


@dp.message_handler(state="edit_phone_number", content_types=["text", "contact"])
async def process_phone_number(message: types.Message, state: FSMContext):
    if message.content_type == "contact":
        phone_number = message.contact.phone_number
        if phone_number.startswith("998"):
            phone_number = "+" + phone_number
    else:
        phone_number = message.text.strip()

    if not validate_phone_number(phone_number):
        await message.answer("Iltimos, telefon raqamingizni +998XXXXXXXXX formatida kiriting!")
        return

    telegram_id = int(message.from_user.id)
    await clsdb.set_phone(phone_number, telegram_id)

    await message.answer(
        text="Telefon raqamingiz muvaffaqiyatli o'zgartirildi!"
    )
    await state.finish()


@dp.callback_query_handler(F.data == "edit_location", state="*")
async def edit_location(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(
        text="Lokasiyani yuboring yoki pastdagi tugmani bosing",
        reply_markup=get_location_dkb()
    )
    await state.set_state("edit_location")


@dp.message_handler(state="edit_location", content_types=["location"])
async def process_location(message: types.Message, state: FSMContext):
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        telegram_id = int(message.from_user.id)

        await clsdb.set_location(latitude, longitude, telegram_id)

        await message.answer(
            text="Lokasiya muvaffaqiyatli o'zgartirildi!", reply_markup=user_main_button(message.from_user.id)
        )
        await state.finish()
    else:
        await message.answer(
            text="Faqat lokasiya yuborilishi lozim!"
        )
