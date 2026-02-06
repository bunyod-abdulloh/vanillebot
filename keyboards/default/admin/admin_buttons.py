from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


def admins_main_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton(
            text="🕸 Web panel",
            web_app=WebAppInfo(url="https://google.com")
        )
    )
    kb.add("✅ Oddiy post yuborish")
    kb.add("🎞 Mediagroup post yuborish")
    kb.add("🏡 Bosh sahifa")

    return kb
