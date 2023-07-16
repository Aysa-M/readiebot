from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_ru import LEXICON_CMDS_RU


async def set_main_menu(bot: Bot):
    """
    Добавляем боту нативную кнопку "Menu" с командами и их описанием.
    Args:
        bot (Bot): активированный бот, в котором происходит работа
    """
    main_menu_cmds = [BotCommand(
        command=command,
        description=description) for command,
                                     description in LEXICON_CMDS_RU.items()]
    await bot.set_my_commands(main_menu_cmds)
