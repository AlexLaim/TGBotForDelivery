from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboards = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Регистрация'
        ),
        KeyboardButton(
            text='Авторизация'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Для продолжения нажмите кнопку ниже')