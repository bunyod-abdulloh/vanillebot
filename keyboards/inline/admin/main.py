from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import WEB_APP_URL


def registration_client_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="📝 Ro'yxatdan o'tish",
            callback_data=f"{WEB_APP_URL}/anketa/"
        )
    )
    return kb
