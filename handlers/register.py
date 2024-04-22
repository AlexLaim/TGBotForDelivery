from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
from utils.database import Database
from passlib.hash import bcrypt
from keyboards.main_menu import main_menu_keyboards
import re


async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = Database()
    user_data = db.get_user_data(message.from_user.id)
    if user_data:
        await bot.send_message(message.from_user.id, text=f'Здравствуйте {user_data[0]} {user_data[2] or ""}! '
                                                          f'Пожалуйста, выберите действие!',
                               reply_markup=main_menu_keyboards)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Начнем регистрацию.\nВведите ваше имя:')
        await state.set_state(RegisterState.regName)


async def register_name(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Введите вашу фамилию:')
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regSurname)


async def register_surname(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Введите ваше отчество (Если у вас его нет, то введите слово: Нет):')
    await state.update_data(regsurname=message.text)
    await state.set_state(RegisterState.regMiddleName)


async def register_middlename(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Введите ваш номер телефона.\n Учтите, что он должен соответствовать такому виду: +7xxxxxxxxxx')
    if message.text == 'Нет':
        await state.update_data(regmiddlename=None)
        await state.set_state(RegisterState.regPhone)
    else:
        await state.update_data(regmiddlename=message.text)
        await state.set_state(RegisterState.regPhone)


async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if(re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text)):
        reg_data = await state.get_data()
        #Дальше достаем переменные из общего массива:
        reg_name = reg_data.get('regname') #Обращаемся к имени, которое писали выше.
        reg_surname = reg_data.get('regsurname')
        reg_middlename = reg_data.get('regmiddlename')
        db = Database()
        id_people = db.check_people(reg_name, reg_surname, reg_middlename, message.text.replace("-", ""))
        if id_people is None:
            id_people = db.add_people(reg_name, reg_surname, reg_middlename, message.text.replace("-", ""))

        if db.check_user(id_people) is False:
            await bot.send_message(message.from_user.id, 'Введите логин, который вы будете использовать для входа:')
            await state.update_data(idPeople=id_people)
            await state.update_data(regphone=message.text.replace("-", ""))
            await state.set_state(RegisterState.regLogin)
        else:
            await bot.send_message(message.from_user.id, 'Данный пользователь уже зарегистрирован. Пожалуйста пройдите авторизацию.')
            await state.clear()

    else:
        await bot.send_message(message.from_user.id, 'Некорректный ввод телефона, введите действительный номер.')


async def register_login(message: Message, state: FSMContext, bot: Bot):
    db = Database()
    if (db.check_login(message.text)):
        await bot.send_message(message.from_user.id, 'Данный логин уже занят. Подберите другой.')
    else:
        await bot.send_message(message.from_user.id, 'Введите пароль, который вы будете использовать для входа.'
                                                     '\nКаким должен быть пароль:'
                                                     '\n• Не менее 12 символов'
                                                     '\n• Не менее 1 заглавной буквы'
                                                     '\n• Не менее 1 специального символа или цифры')
        await state.update_data(reglogin=message.text)
        await state.set_state(RegisterState.regPassword)



async def register_password(message: Message, state: FSMContext, bot: Bot):
    db = Database()
    if (re.findall('^(?=.*[A-ZА-Я])(?=.*[\d\W]).{12,}$', message.text)):
        await state.update_data(regpassword=bcrypt.using(rounds=12).hash(message.text))
        reg_data = await state.get_data()
        # Дальше достаем переменные из общего массива:
        reg_login = reg_data.get('reglogin')
        id_people = reg_data.get('idPeople')
        reg_password = reg_data.get('regpassword')
        db.add_user(id_people, reg_login, reg_password, message.from_user.id)
        await bot.send_message(message.from_user.id, 'Регистрация успешно завершена! Пожалуйста, пройдите авторизацию!')
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Данный пароль ненадежен. Введите другой пароль.'
                                                     '\nКаким должен быть пароль:'
                                                     '\n• Не менее 12 символов'
                                                     '\n• Не менее 1 заглавной буквы'
                                                     '\n• Не менее 1 специального символа или цифры'
                                                     '\nПожалуйста, убедитесь что все условия выполнены')