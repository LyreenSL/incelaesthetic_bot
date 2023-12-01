from aiogram import Router, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from contextlib import suppress

from keyboards.admin_keyboards import \
    get_admin_keyboard, get_post_keyboard, get_delete_keyboard
from main_objects import bot
from middlewares.message_history import SaveMessageMiddleware
from filters.user_rights import UserRightsFilter
from handlers.additional_functions import save_message, delete_all_messages, \
    get_media_object, get_media_answer, get_caption
from database.requests import delete_buttons, posts

router = Router()
router.message.middleware(SaveMessageMiddleware())
router.message.filter(UserRightsFilter(user_rights={'admin', 'superadmin'}))


@router.message(Command('start'))
async def cmd_start(message: Message):
    await save_message(
        await message.answer('Выберите раздел', reply_markup=get_admin_keyboard())
    )


@router.message((F.text == 'CHUD') | (F.text == 'MEMES'))
async def cmd_get_posts(message: Message):
    await delete_all_messages(message.from_user.id)
    for post in await posts.get_as_json(message.text):
        if post['media'] and post['media'][0]['file_type'] in \
                {'photo', 'video', 'audio', 'document'}:
            media_group = [get_media_object(media) for media in post['media']]
            media_group[0] = get_media_object(
                post['media'][0], caption=get_caption(post)
            )
            this_messages = await save_message(
                await message.answer_media_group(media=media_group)
            )

        elif post['media']:
            this_messages = [await save_message(
                await get_media_answer(
                    post['media'][0], message, get_caption(post)
                )
            )]

        else:
            this_messages = [await save_message(
                await message.answer(get_caption(post))
            )]

        answ = await save_message(
            await message.answer(
                '^' * 20, reply_markup=get_post_keyboard(),
            )
        )

        await delete_buttons.add(
            user_id=message.from_user.id, keyboard_id=answ.message_id,
            post_id=post['id'], messages_id=[mes.message_id for mes in this_messages]
        )

    sign = 'CHUD-типирование' if message.text == 'CHUD' else 'Мемы'
    await save_message(
        await message.answer(sign, reply_markup=get_admin_keyboard())
    )


@router.callback_query(F.data == "delete")
async def delete_button(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=get_delete_keyboard()
    )
    if callback.message.caption:
        print(callback.message.caption)


@router.callback_query(F.data == "confirm_delete")
async def delete_button(callback: CallbackQuery):
    button_info = await delete_buttons.get_info(
        callback.message.chat.id, callback.message.message_id
    )
    await posts.remove(button_info['post_id'])
    with suppress(TelegramBadRequest):
        await bot.delete_message(
            callback.message.chat.id, callback.message.message_id
        )
        for mes_id in button_info['messages_id']:
            await bot.delete_message(
                callback.message.chat.id, mes_id
            )


@router.callback_query(F.data == "cancel_delete")
async def delete_button(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=get_post_keyboard()
    )
