from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_admin_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='CHUD')
    builder.button(text='MEMES')
    builder.button(text='RIGHTS')
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_rights_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='/start')
    builder.button(text='/cancel')
    builder.button(text='/add_admin')
    builder.button(text='/remove_admin')
    builder.button(text='/add_to_blacklist')
    builder.button(text='/remove_from_blacklist')
    builder.button(text='/show_admins')
    builder.button(text='/show_blacklist')
    builder.adjust(2, 2, 1, 1, 2)
    return builder.as_markup(resize_keyboard=True)


def get_post_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='удалить', callback_data='delete')
    return builder.as_markup(resize_keyboard=True)


def get_delete_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='точно удалить', callback_data='confirm_delete')
    builder.button(text='отмена', callback_data='cancel_delete')
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
