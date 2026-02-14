from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from data.config import WEB_APP_URL


def registration_client_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="📝 Ro'yxatdan o'tish",
            web_app=WebAppInfo(url=f"{WEB_APP_URL}/client/anketa/")
        )
    )
    return kb
