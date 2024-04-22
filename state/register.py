from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    regName = State()
    regMiddleName = State()
    regSurname = State()
    regPhone = State()
    regLogin = State()
    regPassword = State()
    idPeople = State()