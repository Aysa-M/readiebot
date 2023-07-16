from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDigitCallbackData(BaseFilter):
    """
    Проверка callback_data у объекта CallbackQuery на то, что он состоит из
    цифр, т.е. проверяется действительно ли была нажата кнопка с закладкой -
    номером страницы, на которую нужно перейти.
    Args:
        BaseFilter (_type_): True - если все хорошо, False - если возникает
        ошибка
    """
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    """
    Проверка callback_data от кнопок-закладок, которые нужно удалить в режиме
    редактирования закладок.
    Args:
        BaseFilter (_type_): _description_
    """
    async def __call__(self, callback: CallbackQuery) -> bool:
        return (isinstance(callback.data, str) and 'del' in callback.data and
                callback.data[:-3].isdigit())
