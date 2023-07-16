from copy import deepcopy

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Text

from database.database import user_db, user_dict_template
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.file_handling import BOOK


router_user: Router = Router()


@router_user.message(CommandStart())
async def process_start_command(message: Message):
    """
    Если пользователь отправляет команду /start или активирует бота
    бота из списка, бот приветствует пользователя и сообщает, что пользователь
    может прочитать книгу в чате с ботом, а также предлагает пользователю
    посмотреть список доступных команд, отправив команду /help.
    Также, происходит добавление пользователя в базу данных, если его там еще
    не было.
    Args:
        message (Message): часть объекта update из API telegram
    """
    await message.answer(text=LEXICON_RU['/start'])
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(user_dict_template)


@router_user.message(Command(commands=['help']))
async def process_help_command(message: Message):
    """
    Если пользователь отправляет команду /help, бот присылает пользователю
    список доступных команд, сообщает о том, что можно сохранять страницы
    книги в закладки и желает приятного чтения
    Args:
        message (Message): часть объекта update из API telegram
    """
    await message.answer(text=LEXICON_RU['/help'])


@router_user.message(Command(commands=['beginning']))
async def proccess_beginning_cmd(message: Message):
    """
    Если пользователь отправляет в чат команду /beginning:
    бот отправляет в чат первую страницу книги и 3 инлайн-кнопки (назад,
    текущий номер страницы и вперед)
    Args:
        message (Message): часть объекта update из API telegram
    """
    user_db[message.from_user.id]['page'] = 1
    first_page_txt = BOOK[user_db[message.from_user.id]['page']]
    await message.answer(text=first_page_txt,
                         reply_markup=create_pagination_keyboard(
                            'backward',
                            f"{user_db[message.from_user.id]['page']}/"
                            f"{len(BOOK)}",
                            'forward'))


@router_user.message(Command(commands=['continue']))
async def process_continue_cmd(message: Message):
    """
    Если пользователь отправляет в чат команду /continue:
    бот отправляет в чат страницу книги, на которой пользователь остановил
    чтение во время последнего взаимодействия с сообщением-книгой.
    Если пользователь еще не начинал читать книгу - бот отправляет сообщение с
    первой страницей книги
    Args:
        message (Message): часть объекта update из API telegram
    """
    page_txt = BOOK[user_db[message.from_user.id]['page']]
    await message.answer(
        text=page_txt,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{user_db[message.from_user.id]["page"]}/{len(BOOK)}',
            'forward'))


# Если пользователь отправляет в чат команду /bookmarks возможны несколько
# вариантов сценария:
@router_user.message(Command(commands=['bookmarks']))
async def process_bookmarks_cmd(message: Message):
    """
    1. Если пользователь сохранял закладки ранее, то бот отправляет в чат
    список сохраненных закладок в виде инлайн-кнопок, а также инлайн-кнопки
    "Редактировать" и "Отменить"
    Args:
        message (Message): _description_
    """
    if not user_db[message.from_user.id]['bookmarks']:
        await message.answer(text=LEXICON_RU['no_bookmarks'])
    else:
        await message.answer(text=LEXICON_RU['/bookmarks'],
                             reply_markup=create_bookmarks_keyboard(
            *user_db[message.from_user.id]['bookmarks']))


@router_user.callback_query(Text(text='forward'))
async def process_forward_btn(callback: CallbackQuery):
    """
    Когда пользователь нажимает на кнопку "Вперед", бот загружает следующую
    страницу книги, если текущая страница не последняя. Номер текущей страницы
    на кнопке увеличится на 1. А если текущая страница последняя в книге, то
    ничего не изменится.
    Args:
        callback (CallbackQuery): часть объекта update - CallbackQuery, в
        котором callback data это слово forward - "data": "forward"
                    {
                        "text": ">>",
                        "callback_data": "forward"
                    }
    """
    print(callback.json(indent=4, exclude_none=True))
    if user_db[callback.from_user.id]['page'] < len(BOOK):
        user_db[callback.from_user.id]['page'] += 1
        next_page_txt = BOOK[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=next_page_txt,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{user_db[callback.from_user.id]["page"]}/'
                f'{len(BOOK)}',
                'forward'))
    await callback.answer()


@router_user.callback_query(Text(text='backward'))
async def process_backward_inline_btn(callback: CallbackQuery):
    """
    Когда пользователь нажимает на кнопку "Назад", бот загружает предыдущую
    страницу книги, если текущая страница не первая. Номер текущей страницы
    на кнопке уменьшится на 1. А если текущая страница первая в книге, то
    ничего не изменится.
    Args:
        callback (CallbackQuery): часть объекта update - CallbackQuery, в
        котором callback data это слово backward - "data": "backward"
                    {
                        "text": "<<",
                        "callback_data": "backward"
                    },
    """
    if user_db[callback.from_user.id]['page'] > 1:
        user_db[callback.from_user.id]['page'] -= 1
        prev_page_txt = BOOK[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=prev_page_txt,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{user_db[callback.from_user.id]["page"]}/'
                f'{len(BOOK)}',
                'forward'))
    await callback.answer()


@router_user.callback_query(
        lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_current_page_num(callback: CallbackQuery):
    """
    Когда пользователь нажимает на кнопку с текущим номером страницы и тогда
    бот сохранит эту страницу в закладки, сообщив пользователю об этом
    Args:
        callback (CallbackQuery): часть объекта update - CallbackQuery, в
        котором callback data это номер текущей страницы "data": "1/380"
                    {
                        "text": "1/380",
                        "callback_data": "1/380"
                    },
    """
    user_db[callback.from_user.id]['bookmarks'].add(
        user_db[callback.from_user.id]['page'])
    print(user_db[callback.from_user.id])
    print(callback.json(indent=4, exclude_none=True))
    await callback.answer(text='Добавлено в закладки')


@router_user.callback_query(IsDigitCallbackData())
async def process_press_bookmark_btn(callback: CallbackQuery):
    """
    Если пользователь нажимает на кнопку с закладкой - бот отправляет
    сообщение с книгой на той странице, куда указывает эта закладка
    Args:
        callback (CallbackQuery): часть объекта update - CallbackQuery, в
        котором callback data это номер сохраненной в закладках страницы,
        например "data": "1/380"
    """
    bookmark_page_txt = BOOK[int(callback.data)]
    user_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=bookmark_page_txt,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{user_db[callback.from_user.id]["page"]}/{len(BOOK)}',
            'forward'))
    await callback.answer()


@router_user.callback_query(Text(text='cancel'))
async def process_press_cancel_bookmarks(callback: CallbackQuery):
    """
    Если пользователь нажимает на кнопку "Отменить", то бот убирает список
    закладок и отправляет сообщение с предложением продолжить чтение, отправив
    команду /continue
    Args:
        callback (CallbackQuery): часть объекта update - CallbackQuery
    """
    print(callback.json(indent=4, exclude_none=True))
    await callback.message.answer(text=LEXICON_RU['cancel_text'])
    await callback.answer()


@router_user.callback_query(Text(text='edit_bookmarks'))
async def process_press_edit_bookmarks(callback: CallbackQuery):
    """
    Если пользователь нажимает на кнопку "Редактировать", то бот отправляет
    список сохраненных закладок в виде инлайн-кнопок с пометкой на удаление, а
    также инлайн-кнопку "Отменить"
    Args:
        callback (CallbackQuery): часть объекта update - CallbackQuery
        "data": "edit_bookmarks"
    """
    print(callback.json(indent=4, exclude_none=True))
    await callback.message.answer(text=LEXICON_RU[callback.data],
                                  reply_markup=create_edit_keyboard(
        *user_db[callback.from_user.id]['bookmarks']))
    await callback.answer()


@router_user.callback_query(IsDelBookmarkCallbackData())
async def process_press_del_bookmarks(callback: CallbackQuery):
    """
    Если пользователь нажимает на закладку с пометкой на удаление - она
    пропадает из списка редактируемых закладок
    Args:
        callback (CallbackQuery): часть объекта update - CallbackQuery
        "data": "edit_bookmarks"
    """
    print(callback.json(indent=4, exclude_none=True))
    user_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    if not user_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON_RU['no_bookmarks'])
    else:
        await callback.message.edit_text(text=LEXICON_RU['edit_bookmarks'],
                                         reply_markup=create_edit_keyboard(
            *user_db[callback.from_user.id]['bookmarks']))
    await callback.answer()
