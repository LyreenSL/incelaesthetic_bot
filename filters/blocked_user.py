from database.requests import rights
from aiogram.filters import BaseFilter
from aiogram.types import Message


class BlockedUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        username = message.from_user.username
        if await rights.get(username) == 'blocked':
            await message.answer(
                'Вы заблокированы и не можете отправлять сообщения боту.',
                show_alert=True
            )
            return False
        return True
