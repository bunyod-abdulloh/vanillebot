from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


def admins_main_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton(
            text="🕸 Web panel",
            web_app=WebAppInfo(url="https://google.com")
        )
    )
    kb.add("😎 Foydalanuvchilar soni")
    kb.add("➕ Mijoz qo'shish")
    kb.add("✅ Oddiy post yuborish", "🎞 Mediagroup post yuborish")

    kb.add("🏡 Bosh sahifa")

    return kb
