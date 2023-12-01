from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.admin_keyboards import get_rights_keyboard
from middlewares.message_history import SaveMessageMiddleware
from filters.user_rights import UserRightsFilter
from database.requests import rights
from states.admin_states import AddAdmin, RemoveAdmin, AddBlacklist, RemoveBlacklist
from handlers.additional_functions import save_message, delete_all_messages

router = Router()
router.message.middleware(SaveMessageMiddleware())
router.message.filter(UserRightsFilter(user_rights={'admin', 'superadmin'}))


@router.message(F.text == 'RIGHTS')
async def cmd_get_admin_panel(message: Message):
    await delete_all_messages(message.from_user.id)
    await save_message(
        await message.answer(
            '/start - вернуться к разделам\n'
            '/add_admin - добавить админа (может выполнить только суперадмин)\n'
            '/remove_admin - убрать админа (может выполнить только суперадмин)\n'
            '/add_to_blacklist - добавить пользователя в бан-лист\n'
            '/remove_from_blacklist - убрать пользователя из бан-листа\n'
            '/show_admins - показать список админов\n'
            '/show_blacklist - показать список заблокированных пользователей',
            reply_markup=get_rights_keyboard()
        )
    )


@router.message(Command(commands=[
    'add_admin', 'remove_admin', 'add_to_blacklist', 'remove_from_blacklist'
]))
async def cmd_change_rights(message: Message, state: FSMContext):
    commands = {
        '/add_admin': AddAdmin,
        '/remove_admin': RemoveAdmin,
        '/add_to_blacklist': AddBlacklist,
        '/remove_from_blacklist': RemoveBlacklist
    }
    await save_message(
        await message.answer(
            'Введите имя пользователя, например: @unambomber\n'
            'либо /cancel для отмены.'
        )
    )
    await state.set_state(commands[message.text].username)
    await state.update_data(send=message.text.lower())


@router.message(Command(commands=['cancel']))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await save_message(
        await message.answer('Отменено')
    )


@router.message(F.text, AddAdmin.username)
async def add_admin(message: Message, state: FSMContext):
    username = message.text.replace('@', '').strip()
    user = await rights.get(username)
    admin = await rights.get(message.from_user.username)

    if admin != 'superadmin':
        await save_message(
            await message.answer(
                'У вас нет на это прав'
            )
        )
        await state.clear()
        return

    if user in {'admin', 'superadmin'}:
        await save_message(
            await message.answer(
                'Пользователь уже является админом'
            )
        )
        await state.clear()
        return

    await rights.change(username, 'admin')
    await save_message(
        await message.answer(
            'Пользователю даны права админа'
        )
    )
    await state.clear()


@router.message(F.text, RemoveAdmin.username)
async def remove_admin(message: Message, state: FSMContext):
    username = message.text.replace('@', '').strip()
    user = await rights.get(username)
    admin = await rights.get(message.from_user.username)

    if admin != 'superadmin' or user == 'superadmin':
        await save_message(
            await message.answer(
                'У вас нет на это прав'
            )
        )
        await state.clear()
        return

    if user not in {'superadmin', 'admin'}:
        await save_message(
            await message.answer(
                'Пользователь не является админом'
            )
        )
        await state.clear()
        return

    await rights.change(username, 'member')
    await save_message(
        await message.answer(
            'Пользователь лишён прав админа'
        )
    )
    await state.clear()


@router.message(F.text, AddBlacklist.username)
async def add_admin(message: Message, state: FSMContext):
    username = message.text.replace('@', '').strip()
    user = await rights.get(username)
    admin = await rights.get(message.from_user.username)

    if user == 'superadmin' or \
            (admin != 'superadmin' and user in {'admin', 'superadmin'}):
        await save_message(
            await message.answer(
                'У вас нет на это прав'
            )
        )
        await state.clear()
        return

    if user == 'blocked':
        await save_message(
            await message.answer(
                'Пользователь уже заблокирован'
            )
        )
        await state.clear()
        return

    await rights.change(username, 'blocked')
    await save_message(
        await message.answer(
            'Пользователь заблокирован'
        )
    )
    await state.clear()


@router.message(F.text, RemoveBlacklist.username)
async def remove_admin(message: Message, state: FSMContext):
    username = message.text.replace('@', '').strip()
    user = await rights.get(username)

    if user != 'blocked':
        await save_message(
            await message.answer(
                'Пользователь не заблокирован'
            )
        )
        await state.clear()
        return

    await rights.change(username, 'member')
    await save_message(
        await message.answer(
            'Пользователь разблокирован'
        )
    )
    await state.clear()


@router.message(Command('show_admins'))
async def cmd_change_rights(message: Message):
    users = await rights.get_list('admin') + \
            await rights.get_list('superadmin')
    if not users:
        await save_message(
            await message.answer(
                'Список пуст'
            )
        )
        return

    await save_message(
        await message.answer(
            '\n'.join(['@' + user for user in users])
        )
    )


@router.message(Command('show_blacklist'))
async def cmd_change_rights(message: Message):
    users = await rights.get_list('blocked')
    if not users:
        await save_message(
            await message.answer(
                'Список пуст'
            )
        )
        return

    await save_message(
        await message.answer(
            '\n'.join(['@' + user for user in users])
        )
    )


@router.message()
async def other_message():
    pass
