from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def edit_datas_ikb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            text="👤 Ism sharifni o'zgartirish", callback_data="edit_name"
        )
    )
    kb.add(
        InlineKeyboardButton(
            text="📞 Telefon raqamni o'zgartirish", callback_data="edit_phone"
        )
    )
    return kb
