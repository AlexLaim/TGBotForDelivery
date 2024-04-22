from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

def create_help_kb(page, total_pages, questions):
    kb = InlineKeyboardBuilder()
    questions_per_page = 5  # Количество вопросов на странице
    start_index = page * questions_per_page
    end_index = start_index + questions_per_page

    # Добавляем кнопки для клавиатуры
    for index, (question, answer) in enumerate(list(questions.items())[start_index:end_index]):
        button = InlineKeyboardButton(text=str(question), callback_data=str(start_index + index))
        kb.add(button)

    kb.adjust(1)

    # Добавляем кнопки для навигации по страницам
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"prev_{page}"))
    else:
        buttons.append(InlineKeyboardButton(text="⬅️", callback_data="ignore"))
    buttons.append(InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="ignore"))
    if page < total_pages - 1:
        buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next_{page}"))
    else:
        buttons.append(InlineKeyboardButton(text="➡️", callback_data="ignore"))
    kb.row(*buttons)

    return kb.as_markup()