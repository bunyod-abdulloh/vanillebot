from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsUserJoined(BoundFilter):
    key = "is_user_joined"

    def __init__(self, is_user_joined: bool):
        self.is_user_joined = is_user_joined

    async def check(self, event: types.ChatMemberUpdated):
        if self.is_user_joined:
            return (
                    event.old_chat_member.status in ["left", "kicked"]
                    and event.new_chat_member.status == "member"
            )
        return False


class IsUserLeft(BoundFilter):
    key = "is_user_left"

    def __init__(self, is_user_left: bool):
        self.is_user_left = is_user_left

    async def check(self, event: types.ChatMemberUpdated):
        if self.is_user_left:
            return event.new_chat_member.status in ["left", "kicked"]
        return False
