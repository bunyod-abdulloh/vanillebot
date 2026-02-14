from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser, WebAppInfo

from data.config import WEB_APP_URL


def get_phone_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton(
            text="📞 Telefon raqamni yuborish",
            request_contact=True
        )
    )
    return kb


def get_location_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton(
            text="📍 Lokatsiyani yuborish",
            request_location=True
        )
    )
    return kb

def user_main_button():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🍰 Katalog",  web_app=WebAppInfo(url=f"{WEB_APP_URL[1]}/product"))
            ],
            [
                KeyboardButton(text="🧁 Shaxsiy kabinet"),
                KeyboardButton(text="🍪 Biz haqimizda")
            ],
            [
                KeyboardButton(text="💬 Taklif va shikoyatlar")
            ]
        ],
        resize_keyboard=True
    )
    return markup
