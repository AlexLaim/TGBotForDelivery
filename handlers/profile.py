from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.database import Database
from state.profile import ProfileState
from passlib.hash import bcrypt
from keyboards.profile_kb import profile_keyboards
import re



async def profile_inf(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    db = Database()
    try:
        user_data = db.get_user_data(message.from_user.id)
        await bot.send_message(message.from_user.id,
                                text=f'Данные вашего профиля:'
                                     f'\nИмя: {user_data[0]} '
                                     f'\nФамилия: {user_data[1]}'
                                     f'\nОтчество: {user_data[2] or ""}'
                                     f'\nНомер телефона: {user_data[3]}',
                                reply_markup=profile_keyboards)
    except Exception as Error:
        print('Ошибка при получении данных профиля:', Error)


async def update_data(message: Message, state: FSMContext, bot: Bot):
    try:
        if message.text=='Изменить имя':
            await bot.send_message(message.from_user.id, 'Введите ваше имя:')
            await state.update_data(profName=message.text)
            await state.set_state(ProfileState.ifCommit)
        elif message.text=='Изменить фамилию':
            await bot.send_message(message.from_user.id, 'Введите вашу фамилию:')
            await state.update_data(profSurame=message.text)
            await state.set_state(ProfileState.ifCommit)
        elif message.text=='Изменить отчество':
            await bot.send_message(message.from_user.id, 'Введите ваше отчество:')
            await state.update_data(profMiddlename=message.text)
            await state.set_state(ProfileState.ifCommit)
        elif message.text=='Изменить номер телефона':
            await bot.send_message(message.from_user.id,
                                   'Введите ваш номер телефона.\n Учтите, что он должен соответствовать такому виду: +7xxxxxxxxxx')
            await state.set_state(ProfileState.profPhone)

    except Exception as Error:
        await bot.send_message(message.from_user.id, 'Кажется что-то пошло не так. Попробуйте позже.')
        print('Ошибка при смене имени:', Error)


async def update_phone(message: Message, state: FSMContext, bot: Bot):
    if (re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text)):
        await state.update_data(profPhone=message.text.replace("-", ""))
        try:
            db = Database()
            user_data = db.get_user_data(message.from_user.id)
            id_people = user_data[4]
            prof_data = await state.get_data()
            db.update_people(id_people, name=prof_data.get('profName') or None,
                             surname=prof_data.get('profSurame') or None,
                             middle_name=prof_data.get('profMiddlename') or None,
                             phone_number=prof_data.get('profPhone') or None)
            await bot.send_message(message.from_user.id, 'Данные успешно изменены!')
            user_data = db.get_user_data(message.from_user.id)
            await bot.send_message(message.from_user.id,
                                   text=f'Данные вашего профиля:'
                                        f'\nИмя: {user_data[0]} '
                                        f'\nФамилия: {user_data[1]}'
                                        f'\nОтчество: {user_data[2] or ""}'
                                        f'\nНомер телефона: {user_data[3]}')
            await state.clear()

        except Exception as Error:
            await bot.send_message(message.from_user.id, 'Кажется что-то пошло не так. Попробуйте позже.')
            print('Ошибка при смене имени:', Error)
    else:
        await bot.send_message(message.from_user.id, 'Некорректный ввод телефона, введите действительный номер.')


async def commit_data(message: Message, state: FSMContext, bot: Bot):
    try:
        db = Database()
        user_data = db.get_user_data(message.from_user.id)
        id_people = user_data[4]
        prof_data = await state.get_data()
        key = list(prof_data.keys())[0]
        prof_data[key] = message.text
        db.update_people(id_people, name=prof_data.get('profName') or None, surname=prof_data.get('profSurame') or None,
                         middle_name=prof_data.get('profMiddlename') or None,
                         phone_number=prof_data.get('profPhone') or None)
        await bot.send_message(message.from_user.id, 'Данные успешно изменены!')
        user_data = db.get_user_data(message.from_user.id)
        await bot.send_message(message.from_user.id,
                               text=f'Данные вашего профиля:'
                                    f'\nИмя: {user_data[0]} '
                                    f'\nФамилия: {user_data[1]}'
                                    f'\nОтчество: {user_data[2] or ""}'
                                    f'\nНомер телефона: {user_data[3]}')
        await state.clear()

    except Exception as Error:
        await bot.send_message(message.from_user.id, 'Кажется что-то пошло не так. Попробуйте позже.')
        print('Ошибка при смене имени:', Error)


async def change_pass(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Введите новый пароль.'
                                                 '\nКаким должен быть пароль:'
                                                 '\n• Не менее 12 символов'
                                                 '\n• Не менее 1 заглавной буквы'
                                                 '\n• Не менее 1 специального символа или цифры')
    await state.set_state(ProfileState.newPass)


async def new_pass(message: Message, state: FSMContext, bot: Bot):
    if (re.findall('^(?=.*[A-ZА-Я])(?=.*[\d\W]).{12,}$', message.text)):
        await bot.send_message(message.from_user.id, 'Дла подтверждения введите старый пароль:')
        await state.update_data(newPass=message.text)
        await state.set_state(ProfileState.updatePass)
    else:
        await bot.send_message(message.from_user.id, 'Данный пароль ненадежен. Введите другой пароль.'
                                                     '\nКаким должен быть пароль:'
                                                     '\n• Не менее 12 символов'
                                                     '\n• Не менее 1 заглавной буквы'
                                                     '\n• Не менее 1 специального символа или цифры'
                                                     '\nПожалуйста, убедитесь что все условия выполнены')


async def update_pass(message: Message, state: FSMContext, bot: Bot):
    try:
        db = Database()
        login = db.get_user_login(id_telegram=message.from_user.id)
        dbPass = db.get_user_pass(login)
        if db.check_login(login) and bcrypt.verify(message.text, dbPass):
            prof_data = await state.get_data()
            db.update_pass(message.from_user.id, bcrypt.using(rounds=12).hash(prof_data.get('newPass')))
            await bot.send_message(message.from_user.id, 'Пароль успешно обновлен!')
        else:
            await bot.send_message(message.from_user.id, 'Пароль неверный! Смена пароля не удалась!')
            await state.clear()
    except Exception as Error:
        print('Ошибка проверки пароля при смене:', Error)