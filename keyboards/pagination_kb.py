# Модуль pagination_kb.py отвечает за кнопки под сообщением со страницей книги.
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    """
    Функция принимает строки - кнопки, а возвращает объект клавиатуры, где в
    качестве текстов на кнопках - значения из словаря LEXICON, если
    соответствующие ключи есть в словаре. А если ключа в словаре нет, то текст
    остается таким же, каким был передан в функцию. В качестве callback_data
    передаются значения аргументов функции.
    Returns:
        InlineKeyboardMarkup: _description_
    """
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_RU[btn] if btn in LEXICON_RU else btn,
        callback_data=btn) for btn in buttons])
    return kb_builder.as_markup()
