from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser, WebAppInfo


def get_phone_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton(
            text="📞 Telefon raqamni yuborish",
            request_contact=True
        )
    )
    return kb


def user_main_button():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🍰 Katalog",  web_app=WebAppInfo(url="https://google.com"))
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
