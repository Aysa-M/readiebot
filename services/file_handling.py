# Модуль для преобразования текстового файла книги в словарь, где ключами
# будут номера страниц, а значениями - тексты этих страниц.


BOOK_PATH = 'books/Bredberi_Marsianskie-hroniki.txt'
PAGE_SIZE = 1050  # максимальное количество букв для одной страницы. Число
# 1050 было подобрано опытным путем для экрана моего телефона, чтобы страница
# примерно помещалась в его размеры. У вас это число может быть немного другим.

BOOK: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
# Не работает. Не проходит тесты с пробелами, номер 5
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    """
    Args:
        text (str): строка с полным текстом, из которого нужно получить
        страницу не больше заданного размера
        start (int): номер первого символа в тексте, с которого должна
        начинаться страница (нумерация идет с нуля)
        size (int): максимальный размер страницы, которая должна получиться на
        выходе
    Returns:
        tuple[str, int]: _description_
    """
    symbols: tuple = (',', '.', '!', ':', ';', '?')
    end = 0
    # 1. Определяем вырезанные куски текста, с которыми будем работать далее,
    # обрезая их по определенным правилам.
    if start + size > len(text):
        # Если сумма старт + size больше, чем количество символов в самой
        # последовательности, то сначала найдем максимальный размер size и
        # переопределим его значение, а после этого срежем последовательность
        # по новому значению size
        size = len(text) - start
        # print(size)
        text = text[start: start + size]
    else:
        if (text[start + size] == symbols[1] and
                text[(start + size) - 1] in symbols):
            text = text[start: (start + size) - 2]
            size -= 2
        else:
            text = text[start: start + size]

    # 2. Нужно обрезать текст после символа из списка.
        for i in range(size - 1, 0, -1):
            # print(len(text))
            # print(text[i])
            if text[i] in symbols:
                break
            end = size - i

    # 3. Получаем готовый кусок текста
    page_txt, per_page = text[:size - end], len(text[:size - end])
    return page_txt, per_page


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    """
    Функция должна будет читать файл ____.txt из папки-хранилища books в
    директории проекта и, с помощью функции _get_part_text() преобразовывать
    его в словарь. Ключами в словаре будут идущие подряд номера страниц, а
    значениями - тексты этих страниц.
    Args:
        path (str): строка - путь к файлу с книгой
    """
    with open(path, 'r', encoding='utf-8') as file:
        txt = file.read()
    start, page_num = 0, 1  # номер первого символа в тексте, с которого должна
    # начинаться страница (нумерация идет с нуля)
    while start < len(txt):
        page_txt, per_page = _get_part_text(txt, start, PAGE_SIZE)
        start += per_page
        BOOK[page_num] = page_txt.lstrip()
        page_num += 1


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(BOOK_PATH)
