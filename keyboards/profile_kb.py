from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buttons = [
    KeyboardButton(text='Изменить имя'),
    KeyboardButton(text='Изменить фамилию'),
    KeyboardButton(text='Изменить отчество'),
    KeyboardButton(text='Изменить номер телефона'),
    KeyboardButton(text='Сменить пароль'),
    KeyboardButton(text='Вернуться')
]

# Разделите кнопки на группы по три
keyboard = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]

profile_keyboards = ReplyKeyboardMarkup(
    keyboard=keyboard,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Для продолжение нажмите кнопку ниже'
)