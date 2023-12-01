from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, InputMediaDocument, InputMediaAudio, InputMediaVideo
from contextlib import suppress

from main_objects import bot
from database.requests import messages


async def save_message(answer):
    if type(answer) is not list:
        await messages.save(answer.chat.id, answer.message_id)
        return answer
    for message in answer:
        await messages.save(message.chat.id, message.message_id)
    return answer


async def delete_all_messages(user_id):
    for mes in await messages.get(user_id):
        with suppress(TelegramBadRequest):
            await bot.delete_message(user_id, mes)
    await messages.delete_all(user_id)


def get_caption(post):
    if post["text"] == 'None':
        return f'от: {post["from_user"]}\n' \
               f'дата: {post["date"]}'
    return f'{post["text"]}\n\n' \
           f'от: {post["from_user"]}\n' \
           f'дата: {post["date"]}'


def get_media_dict(message):
    if message.photo:
        return {'file_id': message.photo[-1].file_id, 'file_type': 'photo'}
    elif message.video:
        return {'file_id': message.video.file_id, 'file_type': 'video'}
    elif message.sticker:
        return {'file_id': message.sticker.file_id, 'file_type': 'sticker'}
    elif message.animation:
        return {'file_id': message.animation.file_id, 'file_type': 'animation'}
    elif message.audio:
        return {'file_id': message.audio.file_id, 'file_type': 'audio'}
    elif message.voice:
        return {'file_id': message.voice.file_id, 'file_type': 'voice'}
    elif message.document:
        return {'file_id': message.document.file_id, 'file_type': 'document'}


def get_media_object(media, caption=''):
    if media['file_type'] == 'photo':
        return InputMediaPhoto(media=media['file_id'], caption=caption)
    if media['file_type'] == 'video':
        return InputMediaVideo(media=media['file_id'], caption=caption)
    if media['file_type'] == 'audio':
        return InputMediaAudio(media=media['file_id'], caption=caption)
    if media['file_type'] == 'document':
        return InputMediaDocument(media=media['file_id'], caption=caption)


def get_media_answer(media, message, caption=''):
    if media['file_type'] == 'sticker':
        return message.answer_sticker(
            media['file_id']
        )
    if media['file_type'] == 'animation':
        return message.answer_animation(
            media['file_id'], caption=caption
        )
    if media['file_type'] == 'voice':
        return message.answer_voice(
            media['file_id'], caption=caption
        )
