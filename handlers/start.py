from aiogram import Bot
from aiogram.types import Message
from keyboards.start_kb import start_keyboards
from keyboards.main_menu import main_menu_keyboards
from utils.database import Database

async def get_start(message: Message, bot: Bot):
    db = Database()
    user_data = db.get_user_data(message.from_user.id)
    if user_data:
        await bot.send_message(message.from_user.id, text=f'Здравствуйте {user_data[0]} {user_data[2] or ""}! '
                                                    f'Пожалуйста, выберите действие!', reply_markup=main_menu_keyboards)
    else:
        await bot.send_message(message.from_user.id, text='Доброго времени суток! Данный бот предназначен для клиентов нашей доставки.\n'
                                                      'Пожалуйста, при регистрации или авторизации вводите настоящие данные.', reply_markup=start_keyboards)