# Модуль bookmarks_kb.py отвечает за клавиатуры для работы с закладками
# пользователя.
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU
from services.file_handling import BOOK


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    """
    Функция генерирует список закладок формата {номер страницы} - {Начальный
    текст страницы} в виде инлайн-кнопок (каждая кнопка на новой строке), а
    также еще две кнопки - "Редактировать" и "Отменить":
    Returns:
        InlineKeyboardMarkup: инлайн клавиатура со списком сохраненных
        закладок + с кнопки РЕДАКТИРОВАТЬ и ОТМЕНИТЬ
    """
    # 1. Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # 2. Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for btn in sorted(args):
        kb_builder.row(InlineKeyboardButton(text=f'{btn} - {BOOK[btn][:100]}',
                                            callback_data=str(btn)),
                       width=1)
    # 3. Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    kb_builder.row(InlineKeyboardButton(
        text=LEXICON_RU['edit_bookmarks_button'],
        callback_data='edit_bookmarks'),
                   InlineKeyboardButton(text=LEXICON_RU['cancel'],
                                        callback_data='cancel'),
                   width=2)
    return kb_builder.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    """
    Функция генерирует список закладок к удалению и кнопку "Отменить":
    Returns:
        InlineKeyboardMarkup: _description_
    """
    # 1. Создаем объект клавиатуры
    del_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # 2. Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for del_btn in sorted(args):
        del_kb_builder.row(InlineKeyboardButton(
            text=f"{LEXICON_RU['deleted']}{del_btn} - {BOOK[del_btn][:100]}",
            callback_data=f'{del_btn}del'),
            width=1)
    # 3. Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    del_kb_builder.row(InlineKeyboardButton(text=LEXICON_RU['cancel'],
                                            callback_data='cancel'),
                       width=1)
    return del_kb_builder.as_markup()
