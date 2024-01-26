from aiogram.dispatcher.filters.state import State, StatesGroup


class AuthState(StatesGroup):
    phone = State()
    code = State()