from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def registration_client_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="📝 Ro'yxatdan o'tish",
            callback_data="registration"
        )
    )
    return kb
