from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.member_keyboards import get_member_keyboard
from states.member_states import SendPost
from middlewares.album import AlbumMiddleware
from filters.user_rights import UserRightsFilter
from database.requests import posts
from handlers.additional_functions import get_media_dict

router = Router()
router.message.middleware(AlbumMiddleware())
router.message.filter(UserRightsFilter(user_rights={'member'}))


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        "Это предложка канала Инцелоэстетика.\n"
        "/chud - CHUD-типирование, отправляем одно или несколько личных фото, чтобы вас протипировали.\n"
        "/memes - мемы, отправляем картинки или видео.",
        reply_markup=get_member_keyboard()
    )


@router.message((F.text == 'CHUD') | (F.text == 'MEMES'))
async def cmd_send(message: Message, state: FSMContext):
    await message.answer(
        'Пришлите одно или несколько фото или видео и подпишите при желании:',
        reply_markup=get_member_keyboard()
    )
    await state.set_state(SendPost.send)
    await state.update_data(send=message.text)


@router.message(SendPost.send, F.text)
async def send_post_text(message: Message, state: FSMContext):
    await posts.save(
        post_type=(await state.get_data())["send"],
        from_user=message.from_user.username,
        text=message.text,
        media_list=[]
    )

    await message.answer(
        'Благодарим, рассмотрим.',
        reply_markup=get_member_keyboard()
    )
    await state.clear()


@router.message(
    SendPost.send, F.photo | F.video | F.sticker | F.animation | F.audio | F.voice | F.document
)
async def send_post_album(message: Message, state: FSMContext, album: list):
    media_list = [get_media_dict(mes) for mes in album]

    await posts.save(
        post_type=(await state.get_data())["send"],
        from_user=message.from_user.username,
        text=message.caption,
        media_list=media_list
    )

    await message.answer(
        'Благодарим, рассмотрим.',
        reply_markup=get_member_keyboard()
    )
    await state.clear()


@router.message(SendPost.send)
async def send_post_error(message: Message, state: FSMContext):
    await message.answer(
        'Такой формат контента не принимается, '
        'выберите раздел ещё раз и отправьте '
        'изображение, видео, аудио, гиф, документ или текст.',
        reply_markup=get_member_keyboard()
    )
    await state.clear()


@router.message()
async def send_error(message: Message, state: FSMContext):
    await message.answer(
        'Выберете раздел, прежде чем отправить пост.',
        reply_markup=get_member_keyboard()
    )
    await state.clear()
