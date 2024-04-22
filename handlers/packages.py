import math
from keyboards.main_menu import main_menu_keyboards
from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from utils.database import Database
from state.packages import PackageState
from keyboards.create_pac_kb import create_pac_kb
from keyboards.packages_kb import packages_keyboards
from datetime import datetime

# Поиск посылки
async def get_idPac(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Введите код посылки:')
    await state.set_state(PackageState.idPac)


async def find_pac(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(idPac=message.text)
    db = Database()
    user_data = db.get_user_data(message.from_user.id)
    id_people = user_data[4]
    package_data = db.find_package(message.text, id_people)
    if package_data:
        await bot.send_message(message.from_user.id, f'Посылка найдена, вот информация о ней:'
                                                     f'\nКод посылки: {package_data[0]}'
                                                     f'\nСодержание: {package_data[1]}'
                                                     f'\nОбъем: {package_data[2]} л.'
                                                     f'\nМетод оплаты: {package_data[3]}'
                                                     f'\nПредполагаемая дата доставки: {datetime.strptime(str(package_data[4]), "%Y-%m-%d").strftime("%d.%m.%Y")}'
                                                     f'\nДата заказа: {datetime.strptime(str(package_data[5]), "%Y-%m-%d").strftime("%d.%m.%Y")}'
                                                     f'\nСтоимость: {package_data[6]} руб.'
                                                     f'\nСтатус послыки: {package_data[7]}')
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Посылка не найдена.')


#  Отправленные и ожидаемые посылки

async def get_packages(message: Message, state: FSMContext, bot: Bot):
    try:
        db = Database()
        user_data = db.get_user_data(message.from_user.id)
        id_people = user_data[4]
        if(message.text == 'Ожидаемые посылки'):
            PackageState.packages = db.get_packages(id_people, 'RECIPIENTS')
        else:
            PackageState.packages = db.get_packages(id_people, 'SENDERS')

        if PackageState.packages:
            total_pages = math.ceil(len(PackageState.packages) / 5)  # Рассчитываем общее количество страниц
            await bot.send_message(message.from_user.id, 'Информация о посылках.', reply_markup=packages_keyboards)
            await bot.send_message(message.from_user.id, 'Все найденные посылки:', reply_markup=create_pac_kb(0, total_pages, PackageState.packages))  # Передаем номер страницы и общее количество страниц
            await state.set_state(PackageState.selectPac)
        else:
            await bot.send_message(message.from_user.id, 'Посылки не найдены.')
    except Exception as Error:
        print('Произошла ошибка во время поиска посылок:', Error)


async def select_package(call: CallbackQuery, state: FSMContext):
    db = Database()
    user_data = db.get_user_data(call.from_user.id)
    id_people = user_data[4]
    package_data = db.find_package(call.data, id_people)
    if package_data:
        await call.message.answer(f'Информация о посылке:'
                                  f'\nКод посылки: {package_data[0]}'
                                  f'\nСодержание: {package_data[1]}'
                                  f'\nОбъем: {package_data[2]} л.'
                                  f'\nМетод оплаты: {package_data[3]}'
                                  f'\nПредполагаемая дата доставки: {datetime.strptime(str(package_data[4]), "%Y-%m-%d").strftime("%d.%m.%Y")}'
                                  f'\nДата заказа: {datetime.strptime(str(package_data[5]), "%Y-%m-%d").strftime("%d.%m.%Y")}'
                                  f'\nСтоимость: {package_data[6]} руб.'
                                  f'\nСтатус послыки: {package_data[7]}')
    else:
        # Обрабатываем нажатия на кнопки навигации
        if call.data == "ignore":
            return
        if call.data.startswith("prev_"):
            page = int(call.data.split("_")[1]) - 1
        elif call.data.startswith("next_"):
            page = int(call.data.split("_")[1]) + 1
        else:
            return
        total_pages = math.ceil(len(PackageState.packages) / 5)
        await call.message.edit_reply_markup(reply_markup=create_pac_kb(page, total_pages, PackageState.packages))


async def select_sort_package(call: CallbackQuery, state: FSMContext):
    db = Database()
    user_data = db.get_user_data(call.from_user.id)
    id_people = user_data[4]
    package_data = db.find_package(call.data, id_people)
    if package_data:
        await call.message.answer(f'Информация о посылке:'
                                  f'\nКод посылки: {package_data[0]}'
                                  f'\nСодержание: {package_data[1]}'
                                  f'\nОбъем: {package_data[2]} л.'
                                  f'\nМетод оплаты: {package_data[3]}'
                                  f'\nПредполагаемая дата доставки: {datetime.strptime(str(package_data[4]), "%Y-%m-%d").strftime("%d.%m.%Y")}'
                                  f'\nДата заказа: {datetime.strptime(str(package_data[5]), "%Y-%m-%d").strftime("%d.%m.%Y")}'
                                  f'\nСтоимость: {package_data[6]} руб.'
                                  f'\nСтатус послыки: {package_data[7]}')
    else:
        # Обрабатываем нажатия на кнопки навигации
        if call.data == "ignore":
            return
        if call.data.startswith("prev_"):
            page = int(call.data.split("_")[1]) - 1
        elif call.data.startswith("next_"):
            page = int(call.data.split("_")[1]) + 1
        else:
            return
        total_pages = math.ceil(len(PackageState.packages_sort) / 5)
        await call.message.edit_reply_markup(reply_markup=create_pac_kb(page, total_pages, PackageState.packages_sort))


async def sort_packages(message: Message, state: FSMContext, bot: Bot):
    if PackageState.packages:
        if message.text == 'Сортировать по дате отправки':
            await bot.send_message(message.from_user.id, 'Введите дату в одном из таких форматов:'
                                                         '\nДД.ММ.ГГГГ'
                                                         '\nДо ДД.ММ.ГГГГ'
                                                         '\nПосле ДД.ММ.ГГГГ'
                                                         '\nДД.ММ.ГГГГ-ДД.ММ.ГГГГ')
            await state.set_state(PackageState.dateSort)
    else:
        await bot.send_message(message.from_user.id, text=f'Кажется что-то пошло не так. Попробуйте еще раз.', reply_markup=main_menu_keyboards)


async def date_filter(message: Message, state: FSMContext, bot: Bot):
    PackageState.packages_sort.clear()
    PackageState.filters['Date'] = message.text
    try:
        for package in PackageState.packages:
            package_date = datetime.strptime(str(package[5]), "%Y-%m-%d")
            if 'Date' in PackageState.filters:
                date_filter = PackageState.filters['Date']
                if '-' in date_filter:
                    start_date, end_date = map(lambda x: datetime.strptime(x, "%d.%m.%Y"), date_filter.split('-'))
                    if start_date <= package_date <= end_date:
                        PackageState.packages_sort.append(package)
                elif 'До' in date_filter:
                    end_date = datetime.strptime(date_filter.split(' ')[1], "%d.%m.%Y")
                    if package_date <= end_date:
                        PackageState.packages_sort.append(package)
                elif 'После' in date_filter:
                    start_date = datetime.strptime(date_filter.split(' ')[1], "%d.%m.%Y")
                    if package_date >= start_date:
                        PackageState.packages_sort.append(package)
                else:
                    date = datetime.strptime(date_filter, "%d.%m.%Y")
                    if package_date == date:
                        PackageState.packages_sort.append(package)
        if PackageState.packages_sort:
            total_pages = math.ceil(len(PackageState.packages_sort) / 5)
            await bot.send_message(message.from_user.id, 'Посылки найдены.', reply_markup=packages_keyboards)
            await bot.send_message(message.from_user.id, 'Все найденные посылки:',
                               reply_markup=create_pac_kb(0, total_pages, PackageState.packages_sort))
            await state.set_state(PackageState.sortPac)
        else:
            total_pages = math.ceil(len(PackageState.packages) / 5)
            await bot.send_message(message.from_user.id, 'Посылки по вашему запросу не найдены.')
            await bot.send_message(message.from_user.id, 'Все посылки:',
                                   reply_markup=create_pac_kb(0, total_pages, PackageState.packages))
            await state.set_state(PackageState.selectPac)
    except Exception as Error:
        print('Ошибка при вводе даты сортировки:', Error)
        if isinstance(Error, ValueError):
            await bot.send_message(message.from_user.id, 'Неверный ввод даты. Убедитесь в правильности данных и повторите попытку.')


async def way_filter(message: Message, state: FSMContext, bot: Bot):
    PackageState.packages_sort.clear()
    PackageState.filters['Status'] = 'В пути'
    try:
        for package in PackageState.packages:
            package_status = package[7]
            if 'Status' in PackageState.filters and package_status == PackageState.filters['Status']:
                PackageState.packages_sort.append(package)
        if PackageState.packages_sort:
            total_pages = math.ceil(len(PackageState.packages_sort) / 5)
            await bot.send_message(message.from_user.id, 'Посылки найдены.', reply_markup=packages_keyboards)
            await bot.send_message(message.from_user.id, 'Все найденные посылки:',
                                   reply_markup=create_pac_kb(0, total_pages, PackageState.packages_sort))
            await state.set_state(PackageState.sortPac)
        else:
            total_pages = math.ceil(len(PackageState.packages) / 5)
            await bot.send_message(message.from_user.id, 'Посылки по вашему запросу не найдены.')
            await bot.send_message(message.from_user.id, 'Все посылки:',
                                   reply_markup=create_pac_kb(0, total_pages, PackageState.packages))
            await state.set_state(PackageState.selectPac)
    except Exception as Error:
        print('Ошибка при вводе статуса сортировки:', Error)


async def delivered_filter(message: Message, state: FSMContext, bot: Bot):
    PackageState.packages_sort.clear()
    PackageState.filters['Status'] = 'Доставлено'
    try:
        for package in PackageState.packages:
            package_status = package[7]
            if 'Status' in PackageState.filters and package_status == PackageState.filters['Status']:
                PackageState.packages_sort.append(package)
        if PackageState.packages_sort:
            total_pages = math.ceil(len(PackageState.packages_sort) / 5)
            await bot.send_message(message.from_user.id, 'Посылки найдены.', reply_markup=packages_keyboards)
            await bot.send_message(message.from_user.id, 'Все найденные посылки:',
                                   reply_markup=create_pac_kb(0, total_pages, PackageState.packages_sort))
            await state.set_state(PackageState.sortPac)
        else:
            total_pages = math.ceil(len(PackageState.packages) / 5)
            await bot.send_message(message.from_user.id, 'Посылки по вашему запросу не найдены.')
            await bot.send_message(message.from_user.id, 'Все посылки:',
                                   reply_markup=create_pac_kb(0, total_pages, PackageState.packages))
            await state.set_state(PackageState.selectPac)
    except Exception as Error:
        print('Ошибка при вводе статуса сортировки:', Error)


async def processing_filter(message: Message, state: FSMContext, bot: Bot):
    PackageState.packages_sort.clear()
    PackageState.filters['Status'] = 'В обработке'
    try:
        for package in PackageState.packages:
            package_status = package[7]
            if 'Status' in PackageState.filters and package_status == PackageState.filters['Status']:
                PackageState.packages_sort.append(package)
        if PackageState.packages_sort:
            total_pages = math.ceil(len(PackageState.packages_sort) / 5)
            await bot.send_message(message.from_user.id, 'Посылки найдены.', reply_markup=packages_keyboards)
            await bot.send_message(message.from_user.id, 'Все найденные посылки:',
                                   reply_markup=create_pac_kb(0, total_pages, PackageState.packages_sort))
            await state.set_state(PackageState.sortPac)
        else:
            total_pages = math.ceil(len(PackageState.packages) / 5)
            await bot.send_message(message.from_user.id, 'Посылки по вашему запросу не найдены.')
            await bot.send_message(message.from_user.id, 'Все посылки:',
                                   reply_markup=create_pac_kb(0, total_pages, PackageState.packages))
            await state.set_state(PackageState.selectPac)
    except Exception as Error:
        print('Ошибка при вводе статуса сортировки:', Error)

async def clear_filters(message: Message, state: FSMContext, bot: Bot):
    PackageState.packages_sort.clear()
    PackageState.filters.clear()
    await bot.send_message(message.from_user.id, 'Фильтры успешно очищены!')
    total_pages = math.ceil(len(PackageState.packages) / 5)
    await bot.send_message(message.from_user.id, 'Все посылки:',
                           reply_markup=create_pac_kb(0, total_pages, PackageState.packages))
    await state.set_state(PackageState.selectPac)