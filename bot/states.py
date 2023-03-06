from aiogram.fsm.state import State, StatesGroup


class ChooseState(StatesGroup):
    action = State()
    dif = State()
    notices = State()
