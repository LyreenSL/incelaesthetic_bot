from aiogram.fsm.state import StatesGroup, State


class AddAdmin(StatesGroup):
    username = State()


class RemoveAdmin(StatesGroup):
    username = State()


class AddBlacklist(StatesGroup):
    username = State()


class RemoveBlacklist(StatesGroup):
    username = State()
