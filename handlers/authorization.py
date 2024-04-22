from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.authorization import AuthorizationState
from utils.database import Database
from passlib.hash import bcrypt
from keyboards.main_menu import main_menu_keyboards

async def start_login(message: Message, state: FSMContext, bot: Bot):
    db = Database()
    user_data = db.get_user_data(message.from_user.id)
    if user_data:
        await bot.send_message(message.from_user.id, text=f'Здравствуйте {user_data[0]} {user_data[2] or ""}! '
                                                          f'Пожалуйста, выберите действие!',
                               reply_markup=main_menu_keyboards)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Для авторизации введите ваш логин:')
        await state.set_state(AuthorizationState.autLogin)

async def get_login(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Введите ваш пароль:')
    await state.update_data(autlogin=message.text)
    await state.set_state(AuthorizationState.autPassword)



async def get_password(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(autpassword=message.text)
    aut_data = await state.get_data()
    aut_login = aut_data.get('autlogin')
    aut_pass = aut_data.get('autpassword')
    db = Database()
    dbPass = db.get_user_pass(aut_login)
    if db.check_login(aut_login) and bcrypt.verify(aut_pass, dbPass):
        user_id = db.check_user_data(aut_login)
        db.update_user_tg(message.from_user.id, user_id)
        # Еще не знаю, но тут долджен быть код, который позволит открыть новое меню и запомнить пользователя.
        await bot.send_message(message.from_user.id, 'Авторизация успешно завершена!', reply_markup=main_menu_keyboards)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Неверные логин или пароль.')
        await state.clear()