from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_RU


router_other: Router = Router()


@router_other.message()
async def process_other_msg(message: Message):
    """
    Если пользователь отправляет боту в чат любое другое сообщение, которое не
    предусмотрено логикой обработчиков, бот отвечает фразой.
    Args:
        message (Message): часть объекта update из API telegram
    """
    await message.answer(text=LEXICON_RU['undetected'])
