from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.default.user.user_buttons import user_main_button
from loader import dp, udb


@dp.message_handler(CommandStart(), state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()

    user = await udb.check_user(int(message.from_user.id))

    if user:
        await message.answer(
            text=message.text, reply_markup=user_main_button()
        )
    else:
        await message.answer(
            text="Ism sharifingizni kiriting:"
        )
        await state.set_state("get_full_name")
