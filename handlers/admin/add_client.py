from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from magic_filter import F

from filters import IsBotAdminFilter
from loader import dp


@dp.message_handler(IsBotAdminFilter(), F.text == "➕ Mijoz qo'shish")
async def handle_add_client_main(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(
        text="Mijoz ism-sharifini kiriting"
    )
    await state.set_state("get_client_fullname")


@dp.message_handler(state="get_client_fullname", content_types=["text"])
async def get_client_fullname(message: types.Message, state: FSMContext):
    await state.update_data(client_fullname=message.text)

    await message.answer()