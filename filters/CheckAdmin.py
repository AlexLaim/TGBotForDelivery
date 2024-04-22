import pyodbc
from aiogram.filters import BaseFilter
from aiogram.types import Message
import os
from utils.database import Database
# Класс для дальнейшей работы с администраторами.
# Данный класс создан для того, чтобы в будущем можно было реализовать функционал администратора в боте.
class CheckAdmin(BaseFilter):
    async def __call__(self, message: Message):
        try:
            admin_id = os.getenv('ADMIN_ID')
            db = Database()
            # Данная функция еще не реализована
            user_id = message.from_user.id
        except pyodbc.Error as Error:
            print('Ошибка при поиске администратора')
