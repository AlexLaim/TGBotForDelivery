import pyodbc
from aiogram import Bot
from aiogram.types import Message
from utils.database import Database
from keyboards.start_kb import start_keyboards

async def logout(message: Message, bot: Bot):
    db = Database()
    try:
        db.update_user_tg_null(message.from_user.id)
        await bot.send_message(message.from_user.id,
                                text='Выход успешен. Для продолжение работы нажмите кнопку ниже.',
                                reply_markup=start_keyboards)
    except Exception as Error:
        print('Ошибка при выходе из аккаунта:', Error)
    except pyodbc.Error as Error:
        print('Ошибка при выходе из аккаунта:', Error)