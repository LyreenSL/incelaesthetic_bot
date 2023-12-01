from sqlalchemy import select, delete

from database.requests.main import session_begin
from database.models import Rights


@session_begin
async def get(session, user_id):
    stmt = select(Rights).where(Rights.user_id == user_id)
    user = (await session.scalars(stmt)).all()
    if user:
        return user[0].user_rights
    else:
        return 'member'


@session_begin
async def change(session, user_id, user_rights):
    stmt = select(Rights).where(Rights.user_id == user_id)
    user = (await session.scalars(stmt)).all()
    if user:
        stmt = delete(Rights).where(Rights.user_id == user_id)
        await session.execute(stmt)
    if user_rights != 'member':
        session.add(Rights(user_id=user_id, user_rights=user_rights))
    await session.commit()


@session_begin
async def get_list(session, user_rights):
    stmt = select(Rights).where(Rights.user_rights == user_rights)
    users = (await session.scalars(stmt)).all()
    return [user.user_id for user in users]
