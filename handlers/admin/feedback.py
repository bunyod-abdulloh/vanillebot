from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp, bot


@dp.callback_query_handler(F.data.startswith("feedback_"))
async def feedback_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user_id = call.data.split("_")[1]

    await state.update_data(user_id=user_id)

    await call.message.edit_text(
        text="Javob matnini kiriting"
    )
    await state.set_state("feedback_state")


@dp.message_handler(state="feedback_state")
async def feedback_process(message: types.Message, state: FSMContext):
    data = await state.get_data()

    user_id = data["user_id"]
    user_text = f"Xabaringizga admin javobi:\n\n{message.text}"

    try:
        await bot.send_message(
            chat_id=user_id,
            text=user_text
        )
        admin_text = "Xabar foydalanuvchiga yuborildi!"
    except Exception as err:
        admin_text = f"Xabar foydalanuvchiga yuborilmadi!\n\nSabab:\n\n{err}"

    await message.answer(
        text=admin_text
    )
    await state.finish()
