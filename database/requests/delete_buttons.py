from sqlalchemy import select

from database.requests.main import session_begin
from database.models import DeleteButton


@session_begin
async def add(session, user_id, keyboard_id, post_id, messages_id):
    session.add(DeleteButton(
        user_id=user_id, keyboard_id=keyboard_id, post_id=post_id,
        messages_id=' '.join([str(mes_id) for mes_id in messages_id])
    ))
    await session.commit()


@session_begin
async def get_info(session, user_id, keyboard_id):
    stmt = select(DeleteButton).where(DeleteButton.user_id == user_id)\
        .where(DeleteButton.keyboard_id == keyboard_id)
    button = (await session.scalars(stmt)).all()
    return {
        'post_id': button[0].post_id,
        'messages_id': [
            int(mes_id) for mes_id in button[0].messages_id.split(' ')
        ]
    }
