import asyncio
import logging
from aiogram import Router

from main_objects import bot, dp
from database.requests.main import db_run
from filters.blocked_user import BlockedUserFilter
from handlers import member_handlers, admin_handlers, admin_rights_hendlers


async def main():
    logging.basicConfig(level=logging.INFO)
    ban_router = Router()
    ban_router.message.filter(BlockedUserFilter())
    dp.include_routers(
        ban_router,  member_handlers.router,
        admin_handlers.router, admin_rights_hendlers.router
    )
    await db_run()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
