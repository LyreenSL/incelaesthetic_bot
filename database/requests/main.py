from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_reader import config
from database.models import Base

engine = create_async_engine(config.db_addres)
async_session = async_sessionmaker(engine, expire_on_commit=False)


def session_begin(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            async with session.begin():
                return await func(session, *args, **kwargs)
    return wrapper


async def db_run():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
