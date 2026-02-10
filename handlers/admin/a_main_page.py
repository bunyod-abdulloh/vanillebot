from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from magic_filter import F

from filters import IsBotAdminFilter
from keyboards.default.admin.admin_buttons import admins_main_dkb
from keyboards.default.user.user_buttons import user_main_button
from loader import dp, sdb, udb
from services.helper_functions import send_message_to_users, send_media_group_to_users
from states.admin import AdminSendStates

WARNING_TEXT = (
    "Xabar yuborishdan oldin postingizni yaxshilab tekshirib oling!\n\n"
    "Imkoni bo'lsa postingizni oldin tayyorlab olib keyin yuboring.\n\n"
    "Xabaringizni kiriting:"
)


@dp.message_handler(IsBotAdminFilter(), Command(commands="admin"), state="*")
async def admin_main_page(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(text="Admin panel", reply_markup=admins_main_dkb())


@dp.message_handler(IsBotAdminFilter(), F.text == "😎 Foydalanuvchilar soni", state="*")
async def handle_count_users(message: types.Message, state: FSMContext):
    await state.finish()
    count = await udb.count_users()
    await message.answer(
        text=f"Foydalanuvchilar soni: {count}"
    )


@dp.message_handler(IsBotAdminFilter(), F.text == "✅ Oddiy post yuborish", state="*")
async def send_to_bot_users(message: types.Message):
    send_status = await sdb.get_send_status()
    if send_status:
        await message.answer("Xabar yuborish jarayoni yoqilgan! Hisobot kelganidan so'ng xabar yuborishingiz mumkin!")
    else:
        await message.answer(text=WARNING_TEXT)
        await AdminSendStates.SEND_TO_USERS.set()


@dp.message_handler(state=AdminSendStates.SEND_TO_USERS, content_types=types.ContentTypes.ANY)
async def send_to_bot_users_two(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Xabar yuborish boshlandi!", reply_markup=user_main_button())

    success_count, failed_count = await send_message_to_users(message)

    await sdb.update_status_false()
    await message.answer(
        f"Xabar {success_count} ta foydalanuvchiga yuborildi!\n{failed_count} ta foydalanuvchi botni bloklagan."
    )


@dp.message_handler(IsBotAdminFilter(), F.text == "🎞 Mediagroup post yuborish")
async def send_media_to_bot(message: types.Message):
    send_status = await sdb.get_send_status()
    if send_status:
        await message.answer("Xabar yuborish jarayoni yoqilgan! Hisobot kelganidan so'ng xabar yuborishingiz mumkin!")
    else:
        await message.answer(text=WARNING_TEXT)
        await AdminSendStates.SEND_MEDIA_TO_USERS.set()


@dp.message_handler(state=AdminSendStates.SEND_MEDIA_TO_USERS, content_types=types.ContentTypes.ANY,
                    is_media_group=True)
async def send_media_to_bot_second(message: types.Message, album: List[types.Message], state: FSMContext):
    await state.finish()
    await message.answer(text="Xabar yuborish boshlandi!", reply_markup=user_main_button())
    try:

        media_group = types.MediaGroup()

        for obj in album:
            file_id = obj.photo[-1].file_id if obj.photo else obj[obj.content_type].file_id
            media_group.attach(
                {"media": file_id, "type": obj.content_type, "caption": obj.caption}
            )

    except Exception as err:
        await message.answer(f"Media qo'shishda xatolik!: {err}")
        return

    success_count, failed_count = await send_media_group_to_users(media_group)

    await sdb.update_status_false()
    await message.answer(
        f"Media {success_count} ta foydalanuvchiga yuborildi!\n{failed_count} ta foydalanuvchi botni bloklagan."
    )


@dp.message_handler(F.text == "🏡 Bosh sahifa", state="*")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="Bosh sahifa", reply_markup=user_main_button()
    )
