from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.user.base_ikbs import edit_datas_ikb
from loader import dp, clsdb


@dp.message_handler(F.text == "🧁 Shaxsiy kabinet", state="*")
async def personal_kabinet(message: types.Message, state: FSMContext):
    await state.finish()

    telegram_id = int(message.from_user.id)

    user = await clsdb.check_client(telegram_id)

    if not user:
        await message.answer(
            text="Ushbu bo'limdan foydalanish uchun 💬 Taklif va shikoyatlar bo'limiga yozing, admin Sizni mijozlarimiz "
                 "safiga qo'shib qo'yadi"
        )
        # await message.answer(
        #     text="Mahsulotlarimizdan buyurtma qilish uchun ism-sharif, telefon raqam va yetkazib berishimiz uchun lokatsiyangizni kiritishingiz lozim!",
        #     reply_markup=add_personal_datas_ikb()
        # )
    else:
        data = await clsdb.get_client(telegram_id)
        full_name = data["full_name"]
        phone = data["phone"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        await message.answer_location(latitude, longitude)
        await message.answer(
            text=f"Ism - sharif: {full_name}\n"
                 f"Telefon raqam: {phone}\n\n"
                 f"O'zgartirmoqchi bo'lsangiz kerakli tugmani bosing",
            reply_markup=edit_datas_ikb()
        )
