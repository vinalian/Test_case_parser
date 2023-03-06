from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from bot.database import Bot_connection


class Notices(CallbackData, prefix='a'):
    action: str
    data: str


def main():
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Подборка задач", callback_data='Choose_task'))
    return kb.as_markup()


def back_main():
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="В меню", callback_data='back'))
    return kb.as_markup()


def choose_notices():
    con = Bot_connection()
    data = con.get_all_notices()
    kb = InlineKeyboardBuilder()
    for note in data:
        if len(note[0].split(',')) == 1:
            kb.row(types.InlineKeyboardButton(text=note[0], callback_data=Notices(
                action='notices',
                data=note[0]
            ).pack()))
    kb.row(types.InlineKeyboardButton(text="В меню", callback_data='back'))
    return kb.as_markup()


def choose_dif(notices):
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


def link(url):
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Страница на сайте", url=url))
    return kb.as_markup()
