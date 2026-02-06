from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from magic_filter import F

from loader import dp, udb
from services.helper_functions import validate_full_name, validate_phone_number


@dp.callback_query_handler(F.data == "edit_name", state="*")
async def edit_full_name(call: CallbackQuery, state: FSMContext):
    await state.finish()

    text = "Yangi ism - familiyangizni kiriting:"
    await call.message.edit_text(text)
    await state.set_state("edit_full_name")


@dp.message_handler(state="edit_full_name")
async def process_full_name(message, state: FSMContext):
    full_name = message.text.strip()

    if not validate_full_name(full_name):
        await message.answer(
            "Iltimos, ism va familiyangizni lotincha, bitta probel bilan kiriting"
        )
        return
    telegram_id = int(message.from_user.id)
    await udb.set_full_name(telegram_id, full_name)

    await message.answer(
        text="Ism - familiyangiz muvaffaqiyatli o'zgartirildi!"
    )
    await state.finish()


@dp.callback_query_handler(F.data == "edit_phone", state="*")
async def edit_phone_number(call: CallbackQuery, state: FSMContext):
    await state.finish()

    text = "Yangi telefon raqamingizni kiriting:\n\nFormat: +998XXXXXXXXX"
    await call.message.edit_text(text)
    await state.set_state("edit_phone_number")


@dp.message_handler(state="edit_phone_number", content_types=["text", "contact"])
async def process_phone_number(message, state: FSMContext):
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
    await udb.set_phone_number(telegram_id, phone_number)

    await message.answer(
        text="Telefon raqamingiz muvaffaqiyatli o'zgartirildi!"
    )
    await state.finish()
