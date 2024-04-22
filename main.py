# Для библиотек
import os
import asyncio
import pyodbc
from aiogram import Bot, Dispatcher, types, filters, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
# Файлы с методами
from utils.commands import set_commands
# Классы с данными
from state.register import RegisterState
from state.authorization import AuthorizationState
from state.profile import ProfileState
# Хендлеры
from handlers.start import get_start
from handlers.help import *
from handlers.register import *
from handlers.authorization import *
from handlers.logout import *
from handlers.profile import *
from handlers.back_menu import *
from handlers.packages import *


load_dotenv()
token = os.getenv('TOKEN')
# Создаем бота
bot = Bot(token=os.getenv('TOKEN'))
# Создаем диспетчер
dp = Dispatcher()


dp.message.register(get_start, filters.Command(commands='start'))
dp.message.register(help, filters.Command(commands='help'))

async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


# Хендлер регистрации
dp.message.register(start_register, F.text=='Регистрация')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_surname, RegisterState.regSurname)
dp.message.register(register_middlename, RegisterState.regMiddleName)
dp.message.register(register_phone, RegisterState.regPhone)
dp.message.register(register_login, RegisterState.regLogin)
dp.message.register(register_password, RegisterState.regPassword)

# Хендлер авторизации
dp.message.register(start_login, F.text=='Авторизация')
dp.message.register(get_login, AuthorizationState.autLogin)
dp.message.register(get_password, AuthorizationState.autPassword)

# Хендлер возврата в меню
dp.message.register(back_menu, F.text=='Вернуться')

# Хендлер выхода
dp.message.register(logout, F.text=='Выйти из аккаунта')

# Хендлеры профиля
dp.message.register(profile_inf, F.text=='Профиль')
dp.message.register(update_data, F.text=='Изменить имя')
dp.message.register(update_data, F.text=='Изменить фамилию')
dp.message.register(update_data, F.text=='Изменить отчество')
dp.message.register(update_data, F.text=='Изменить номер телефона')
dp.message.register(update_phone, ProfileState.profPhone)
dp.message.register(commit_data, ProfileState.ifCommit)
dp.message.register(change_pass, F.text=='Сменить пароль')
dp.message.register(new_pass, ProfileState.newPass)
dp.message.register(update_pass, ProfileState.updatePass)

# Хендлер поддержки
dp.message.register(start_help, F.text=='Поддержка')
dp.message.register(questions, F.text=='Частые вопросы')
dp.callback_query.register(select_question, HelpState.selectQuestion)
# Хендлер посылок
# Поиск
dp.message.register(get_idPac, F.text=='Найти посылку')
dp.message.register(find_pac, PackageState.idPac)
# Список посылок
dp.message.register(get_packages, F.text=='Отправленные посылки')
dp.message.register(get_packages, F.text=='Ожидаемые посылки')
dp.callback_query.register(select_package, PackageState.selectPac)
# Сортировки
dp.message.register(clear_filters, F.text=='Очистить фильтры')
dp.message.register(sort_packages, F.text=='Сортировать по дате отправки')
dp.message.register(date_filter, PackageState.dateSort)
dp.message.register(delivered_filter, F.text=='Доставленные')
dp.message.register(processing_filter, F.text=='Ожидают доставки')
dp.message.register(way_filter, F.text=='В пути')
dp.callback_query.register(select_sort_package, PackageState.sortPac)

if __name__ == '__main__':
    asyncio.run(start())
