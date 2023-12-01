from database.requests import rights
from aiogram.filters import BaseFilter
from aiogram.types import Message


class UserRightsFilter(BaseFilter):
    def __init__(self, user_rights: set[str]):
        self.user_rights = user_rights

    async def __call__(self, message: Message) -> bool:
        username = message.from_user.username
        return await rights.get(username) in self.user_rights
