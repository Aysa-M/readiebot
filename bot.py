import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_credentials
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu


logger = logging.getLogger(__name__)


async def main():
    # Конфигурация логирования
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                               '[%(asctime)s] - %(name)s - %(message)s')
    logging.info('Starting bot')

    # Загружаем конфиг в переменную config и нициализируем бот и диспетчер
    config: Config = load_credentials('.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dispatcher: Dispatcher = Dispatcher()

    # Устанавливаем нативную кнопку меню при старте бота
    await set_main_menu(bot=bot)

    # Регистриуем роутеры в диспетчере
    dispatcher.include_router(user_handlers.router_user)
    dispatcher.include_router(other_handlers.router_other)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


# python bot.py
