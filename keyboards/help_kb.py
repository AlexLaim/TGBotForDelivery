from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buttons = [
    KeyboardButton(
                text='Частые вопросы'
            ),
            KeyboardButton(
                text='Вернуться'
            )
]

keyboard = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]

help_keyboards = ReplyKeyboardMarkup(
    keyboard=keyboard,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Для продолжения нажмите кнопку ниже'
)