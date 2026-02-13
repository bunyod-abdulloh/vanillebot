from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from magic_filter import F

from keyboards.default.user.user_buttons import get_location_dkb
from loader import dp
from services.helper_functions import validate_full_name, validate_phone_number


@dp.callback_query_handler(F.data == "registration", state="*")
async def handle_registration(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Ism-sharifingizni kiriting"
    )
    await state.set_state("get_client_fullname")


@dp.message_handler(state="get_client_fullname", content_types=["text"])
async def get_client_fullname(message: types.Message, state: FSMContext):
    full_name = message.text.strip()

    if not validate_full_name(full_name):
        await message.answer(
            "Iltimos, ism va familiyangizni lotincha, bitta probel bilan kiriting"
        )
        return

    await state.update_data(client_fullname=full_name)

    await message.answer(
        text="Telefon raqamingizni kiriting\n\nFormat: +998XXXXXXXXX\n\nYoki pastdagi tugmani bosing va kontaktni "
             "yuboring.", reply_markup=get_phone_dkb()
    )

    await state.set_state("get_client_phone")


@dp.message_handler(state="get_client_phone", content_types=["text", "contact"])
async def get_client_phone(message: types.Message, state: FSMContext):
    if message.content_type == "contact":
        phone = message.contact.phone_number
        if phone.startswith("998"):
            phone = "+" + phone
    else:
        phone = message.text.strip()

    if not validate_phone_number(phone):
        await message.answer("Iltimos, telefon raqamingizni +998XXXXXXXXX formatida kiriting!")
        return

    await state.update_data(client_phone=phone)

    await message.answer(
        text="Lokatsiyangizni yuboring yoki pastdagi tugmani bosing", reply_markup=get_location_dkb()
    )
    await state.set_state("get_client_location")


@dp.message_handler(state="get_client_location", content_types=["location"])
async def get_client_location(message: types.Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude

    await state.update_data(client_location=[latitude, longitude])

    await message.answer(
        text="Do'kon nomini kiriting"
    )
    await state.set_state("get_client_shop")


@dp.message_handler(state="get_client_shop", content_types=["text"])
async def get_client_shop(message: types.Message, state: FSMContext):
    shop_name = message.text.strip()

    await state.update_data(shop_name=shop_name)

    await message.answer(
        text="Do'kon filiali bormi?"
    )