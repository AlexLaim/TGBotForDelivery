from aiogram.fsm.state import StatesGroup, State

class AuthorizationState(StatesGroup):
    autLogin = State()
    autPassword = State()