from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.default.user.user_buttons import get_phone_dkb, user_main_button, get_location_dkb
from keyboards.inline.user.base_ikbs import add_personal_datas_ikb
from loader import dp, udb, clsdb
from services.helper_functions import validate_full_name, validate_phone_number


@dp.callback_query_handler(F.data == "add_personal_data", state="*")
async def add_personal_data(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Ism-sharifingizni kiriting"
    )
    await state.set_state("get_full_name")


@dp.message_handler(state="get_full_name")
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text.strip()

    if not validate_full_name(full_name):
        await message.answer(
            "Iltimos, ism va familiyangizni lotincha, bitta probel bilan kiriting"
        )
        return

    await state.update_data(fullname=full_name)

    await message.answer(
        text="Telefon raqamingizni kiriting\n\nFormat: +998XXXXXXXXX\n\nYoki pastdagi tugmani bosing va kontaktni "
             "yuboring.", reply_markup=get_phone_dkb()
    )
    await state.set_state("get_phone_number")


@dp.message_handler(state="get_phone_number", content_types=["text", "contact"])
async def get_phone_number(message: types.Message, state: FSMContext):
    if message.content_type == "contact":
        phone = message.contact.phone_number
        if phone.startswith("998"):
            phone = "+" + phone
    else:
        phone = message.text.strip()

    if not validate_phone_number(phone):
        await message.answer("Iltimos, telefon raqamingizni +998XXXXXXXXX formatida kiriting!")
        return

    await state.update_data(phone=phone)

    await message.answer(
        text="Lokatsiyangizni yuboring yoki pastdagi tugmani bosing", reply_markup=get_location_dkb()
    )

    await state.set_state("get_location")


@dp.message_handler(state="get_location", content_types=["location"])
async def get_location(message: types.Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude

    data = await state.get_data()

    if len(data) != 2:
        await message.answer(
            text="Xatolik!\n\nMa'lutmotlaringizni qayta kiritiing",
            reply_markup=add_personal_datas_ikb()
        )
        await state.finish()

    telegram_id = int(message.from_user.id)
    full_name = data['fullname']
    phone = data['phone']

    await clsdb.add_client(
        telegram_id=telegram_id, full_name=full_name, phone=phone,
        latitude=latitude, longitude=longitude
    )

    await message.answer_location(latitude, longitude)

    await message.answer(
        text=f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\nIsm sharifingiz: {full_name}\n"
             f"Telefon raqamingiz: {phone}",
        reply_markup=user_main_button()
    )
    await state.finish()
