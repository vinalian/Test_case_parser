from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from bot.database import Bot_connection


class Notices(CallbackData, prefix='a'):
    action: str
    data: str


def main() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Подборка задач", callback_data='Choose_task'))
    return kb.as_markup()


def back_main() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="В меню", callback_data='back'))
    return kb.as_markup()


def choose_notices() -> types.InlineKeyboardMarkup:
    con = Bot_connection()
    data = con.get_all_notices()
    kb = InlineKeyboardBuilder()
    data_list = []
    for note in data:
        if note[0] not in data_list:
            data_list.append(note[0])
            if len(data_list) % 2 == 0:
                kb.row(types.InlineKeyboardButton(text=note[0], callback_data=Notices(
                    action='notices',
                    data=note[1]
                ).pack()))
            else:
                kb.add(types.InlineKeyboardButton(text=note[0], callback_data=Notices(
                    action='notices',
                    data=note[1]
                ).pack()))
    kb.row(types.InlineKeyboardButton(text="В меню", callback_data='back'))
    return kb.as_markup()


def choose_dif(notices: str) -> types.InlineKeyboardMarkup:
    con = Bot_connection()
    data = con.get_dif(notices)
    kb = InlineKeyboardBuilder()
    for dif in data:
        kb.row(types.InlineKeyboardButton(text=dif[0], callback_data=Notices(
            action='dif',
            data=dif[0]
        ).pack()))
    kb.row(types.InlineKeyboardButton(text="В меню", callback_data='back'))
    return kb.as_markup()


def more_info(id: int) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Показать подробнее", callback_data=Notices(action='more_info',
                                                                                       data=id).pack()))
    return kb.as_markup()


def link(url: str) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Ссылка на сайт", url=url, callback_data="#"))
    return kb.as_markup()
