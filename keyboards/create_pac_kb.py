from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

def create_pac_kb(page, total_pages, packages):
    kb = InlineKeyboardBuilder()
    packages_per_page = 5  # Количество посылок на странице
    start_index = page * packages_per_page
    end_index = start_index + packages_per_page

    # Добавляем кнопки для клавиатуры
    for pac in packages[start_index:end_index]:
        button = InlineKeyboardButton(text=str(pac[0]), callback_data=str(pac[0]))
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


