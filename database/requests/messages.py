from sqlalchemy import select, delete

from database.requests.main import session_begin
from database.models import MessageID, DeleteButton


@session_begin
async def save(session, user_id, message_id):
    session.add(MessageID(user_id=user_id, message_id=message_id))
    await session.commit()


@session_begin
async def get(session, user_id):
    stmt = select(MessageID).where(MessageID.user_id == user_id)
    messages = (await session.scalars(stmt)).all()
    await session.commit()
    return [await mes.awaitable_attrs.message_id for mes in messages]


@session_begin
async def delete_all(session, user_id):
    stmt = delete(MessageID).where(MessageID.user_id == user_id)
    await session.execute(stmt)
    stmt = delete(DeleteButton).where(DeleteButton.user_id == user_id)
    await session.execute(stmt)
    await session.commit()
