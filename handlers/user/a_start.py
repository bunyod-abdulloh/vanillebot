from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.default.user.user_buttons import user_main_button
from loader import dp, udb


@dp.message_handler(CommandStart(), state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()

    telegram_id = int(message.from_user.id)
    user = await udb.check_user(telegram_id)

    if not user:
        await udb.add_user(telegram_id)

    await message.answer(
        text=message.text, reply_markup=user_main_button(message.from_user.id)
    )
