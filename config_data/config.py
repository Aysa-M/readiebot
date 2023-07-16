from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_credentials(path: str | None):
    """
    Создаем функцию, которая будет читать файл .env и возвращать экземпляр
    класса Config с заполненными полями token и admin_ids
    Args:
        path (str | None): _description_
    """
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=env('ADMIN_ID')))
