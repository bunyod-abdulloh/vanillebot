from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def add_personal_datas_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="🧁 Shaxsiy ma'lumotlarni kiritish", callback_data="add_personal_data"
        )
    )
    return kb

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
    kb.add(
        InlineKeyboardButton(
            text="📍 Lokasiyani o'zgartirish", callback_data="edit_location"
        )
    )
    return kb


def feedback_ikb(telegram_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            text="Javob berish", callback_data=f"feedback_{telegram_id}"
        )
    )
    return kb
