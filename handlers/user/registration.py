from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from magic_filter import F

from loader import dp


@dp.callback_query_handler(F.data == "registration", state="*")
async def handle_registration(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Ism-sharifingizni kiriting"
    )
    await state.set_state("get_client_fullname")


@dp.message_handler(state="get_client_fullname", content_types=["text"])
async def get_client_fullname(message: types.Message, state: FSMContext):
    await state.update_data(client_fullname=message.text)

    await message.answer(
        text="Telefon raqamingizni kiriting"
    )

    await state.set_state("get_client_phone")


@dp.message_handler(state="get_client_phone", content_types=["text"])
async def get_client_phone(message: types.Message, state: FSMContext):
    pass
