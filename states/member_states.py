from aiogram.fsm.state import StatesGroup, State


class SendPost(StatesGroup):
    send = State()
