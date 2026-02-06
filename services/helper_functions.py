import asyncio
import re

import aiogram
from aiogram import types

from loader import bot, udb, sdb
from services.error_service import notify_exception_to_admin


def extracter(items, delimiter):
    empty_list = []
    for e in range(0, len(items), delimiter):
        empty_list.append(items[e:e + delimiter])
    return empty_list


FULL_NAME_PATTERN = re.compile(
    r"^[A-Za-zʼ'ʻ]+( [A-Za-zʼ'ʻ]+){0,3}$"
)

PHONE_PATTERN = re.compile(r"^\+998\d{9}$")


def validate_full_name(full_name: str, max_length: int = 30) -> bool:
    if not full_name:
        return False

    if len(full_name) > max_length:
        return False

    return bool(FULL_NAME_PATTERN.fullmatch(full_name))


def validate_phone_number(phone_number: str) -> bool:
    if not phone_number:
        return False

    return bool(PHONE_PATTERN.fullmatch(phone_number))


async def send_message_to_users(message: types.Message):
    await sdb.update_status_true()
    all_users = await udb.select_all_users()
    success_count, failed_count = 0, 0

    for index, user in enumerate(all_users, start=1):
        try:
            await message.copy_to(chat_id=user["telegram_id"])
            success_count += 1
        except aiogram.exceptions.BotBlocked:
            failed_count += 1
            await udb.delete_user(user["telegram_id"])
        except aiogram.exceptions.UserDeactivated:
            failed_count += 1
            await udb.delete_user(user["telegram_id"])
        except aiogram.exceptions.ChatNotFound:
            failed_count += 1
            await udb.delete_user(user["telegram_id"])
        except Exception as err:
            await notify_exception_to_admin(err=err)
        if index % 1500 == 0:
            await asyncio.sleep(30)
        await asyncio.sleep(0.05)

    return success_count, failed_count


async def send_media_group_to_users(media_group: types.MediaGroup):
    await sdb.update_status_true()
    all_users = await udb.select_all_users()
    success_count, failed_count = 0, 0

    for index, user in enumerate(all_users, start=1):
        try:
            await bot.send_media_group(chat_id=user['telegram_id'], media=media_group)
            success_count += 1
        except aiogram.exceptions.BotBlocked:
            failed_count += 1
            await udb.delete_user(user["telegram_id"])
        except aiogram.exceptions.UserDeactivated:
            failed_count += 1
            await udb.delete_user(user["telegram_id"])
        except aiogram.exceptions.ChatNotFound:
            failed_count += 1
            await udb.delete_user(user["telegram_id"])
        except Exception as err:
            await notify_exception_to_admin(err=err)
        if index % 1500 == 0:
            await asyncio.sleep(30)
        await asyncio.sleep(0.05)

    return success_count, failed_count
