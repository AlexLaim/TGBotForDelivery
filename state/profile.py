from aiogram.fsm.state import StatesGroup, State

class ProfileState(StatesGroup):
    profPhone = State()
    ifCommit = State()
    newPass = State()
    updatePass = State()