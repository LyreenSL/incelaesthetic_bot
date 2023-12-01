from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from database.requests.main import session_begin
from database.models import Post, Media


@session_begin
async def save(session, post_type, from_user, text, media_list):
    session.add(Post(
            post_type=post_type, from_user=f'@{from_user}', text=text,
            media=[Media(
                file_id=media['file_id'], file_type=media['file_type']
            ) for media in media_list]
    ))
    await session.commit()


@session_begin
async def remove(session, post_id):
    stmt = delete(Media).where(Media.post_id == post_id)
    await session.execute(stmt)
    stmt = delete(Post).where(Post.id == post_id)
    await session.execute(stmt)


@session_begin
async def get_as_json(session, post_type):
    stmt = select(Post).options(selectinload(Post.media))\
        .where(Post.post_type == post_type)
    return reversed([{
        'id': post.id,
        'text': f'{post.text}',
        'from_user': f'{post.from_user}',
        'date': f'{post.date}',
        'media': [{
            'file_id': media.file_id,
            'file_type': media.file_type
        } for media in post.media]
    } for post in (await session.execute(stmt)).scalars()])
