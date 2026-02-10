from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from magic_filter import F

from keyboards.inline.admin.main import registration_client_ikb
from loader import dp, bot


@dp.callback_query_handler(F.data.startswith("client_"))
async def handle_add_client_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    client_telegram = int(call.data.split("_")[1])

    try:
        await bot.send_message(
            chat_id=client_telegram,
            text="Admin ro'yxatdan o'tish uchun ruxsat berdi!",
            reply_markup=registration_client_ikb()
        )

        admin_text = "Ruxsat xabari foydalanuvchiga yuborildi!"

    except Exception as err:
        admin_text = f"Ruxsat xabari foydalanuvchiga yetib bormadi! Sabab:\n\n{err}"

    await call.message.edit_text(
        text=admin_text
    )
