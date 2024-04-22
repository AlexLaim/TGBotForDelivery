from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboards = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправленные посылки'
        ),
        KeyboardButton(
            text='Ожидаемые посылки'
        ),
        KeyboardButton(
            text='Найти посылку'
        ),
    ],
    [
        KeyboardButton(
            text='Поддержка'
        ),
        KeyboardButton(
            text='Профиль'
        ),
        KeyboardButton(
            text='Выйти из аккаунта'
        ),
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Для продолжения нажмите кнопку ниже')