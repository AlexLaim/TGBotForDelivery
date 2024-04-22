from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.packages import PackageState
from keyboards.main_menu import main_menu_keyboards

async def back_menu(message: Message, state: FSMContext, bot: Bot):
    if PackageState.isPeople:
        PackageState.isPeople = False
    await bot.send_message(message.from_user.id, text=f'Пожалуйста, выберите действие!', reply_markup=main_menu_keyboards)
    await state.clear()