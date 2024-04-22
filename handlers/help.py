import math

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.start_kb import start_keyboards
from keyboards.main_menu import main_menu_keyboards
from keyboards.help_kb import help_keyboards
from keyboards.create_help_kb import create_help_kb
from state.help import HelpState
from utils.database import Database

async def help(message: Message, bot: Bot):
    db = Database()
    user_data = db.get_user_data(message.from_user.id)
    if user_data:
        await bot.send_message(message.from_user.id, text=f'Здравствуйте {user_data[0]} {user_data[2] or ""}!\n'
                                                    f'Данный бот создан для просмотра информации о посылках!\n'
                                                    f'Если вы столкнулись с проблемой, пожете обратиться к поддержке по кнопке ниже.', reply_markup=main_menu_keyboards)
    else:
        await bot.send_message(message.from_user.id, text='Доброго времени суток! Данный бот предназначен для клиентов нашей доставки.\n'
                                                      'Пожалуйста, для работы с ним необходимо пройти авторизацию по кнопке ниже.', reply_markup=start_keyboards)


async def start_help(message: Message, bot: Bot):
    db = Database()
    user_data = db.get_user_data(message.from_user.id)
    await bot.send_message(message.from_user.id, text=f'Здравствуйте {user_data[0]} {user_data[2] or ""}!\n'
                                                      f'Прежде чем задавать вопросы, пожалуйста, ознакомьтесь с частыми случаями,'
                                                      f' возможно ответ на ваш вопрос будет именно там!\n'
                                                      f'Если вы не нашли ответа, пожалуйста напишите нам на почту свой вопрос: help@delivery.ru',
                           reply_markup=help_keyboards)


async def questions(message: Message, state: FSMContext, bot: Bot):
    total_pages = math.ceil(len(HelpState.questions.keys()) / 5)
    await bot.send_message(message.from_user.id, 'Ниже приведен список частых вопросов.\n'
                                                 'Если вы не нашли ответа на свой вопрос, пожалуйста свяжитесь с нами по почте: help@delivery.ru'
                           , reply_markup=create_help_kb(0, total_pages, HelpState.questions))
    await state.set_state(HelpState.selectQuestion)


async def select_question(call: CallbackQuery, state: FSMContext):
    keys_list = list(HelpState.questions.keys())
    if call.data.isdigit():
        index = int(call.data)
        key = keys_list[index]
        await call.message.answer(f'{key}\n{HelpState.questions[key]}')
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
        total_pages = math.ceil(len(HelpState.questions.keys()) / 5)
        await call.message.edit_reply_markup(reply_markup=create_help_kb(page, total_pages, HelpState.questions))
