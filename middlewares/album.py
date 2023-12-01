import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):

    def __init__(self, *args):
        self.album_data: dict = {}
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not message.media_group_id:
            data['album'] = [message]
            return await handler(message, data)
        try:
            self.album_data[message.media_group_id].append(message)
            return
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(0.01)
            data['album'] = self.album_data[message.media_group_id]

            res = await handler(message, data)
            del self.album_data[message.media_group_id]
            return res
