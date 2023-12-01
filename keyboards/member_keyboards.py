from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_member_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text='CHUD')
    builder.button(text='MEMES')
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
