from aiogram import Router, types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from states import ChooseState
from bot import database as DB
from bot import keyboard as KB
from magic_filter import F
from run_bot import bot
import asyncio

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Это бот для получения задач!\n",
        reply_markup=KB.main())


@router.callback_query(Text('back'))
async def back_main(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        'Вы вернулись в меню',
        reply_markup=KB.main()
    )


@router.callback_query(Text('Choose_task'))
async def choose_task(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        'Выбери тему',
        reply_markup=KB.choose_notices()
    )
    await state.set_state(ChooseState.notices)


@router.callback_query(KB.Notices.filter(F.action == 'notices'))
async def choose_difficulty(call: types.CallbackQuery, state: FSMContext, callback_data: KB.Notices):
    await state.update_data(notices=callback_data.data)
    await call.message.edit_text(
        'Теперь выберем сложность',
        reply_markup=KB.choose_dif(callback_data.data)
    )
    await state.set_state(ChooseState.dif)


@router.callback_query(KB.Notices.filter(F.action == 'dif'))
async def choose_difficulty(call: types.CallbackQuery, state: FSMContext, callback_data: KB.choose_dif):
    data = await state.get_data()
    con = DB.Bot_connection()
    all_topic = con.get_data(
        difficulty=callback_data.data,
        id=data['notices'])
    await call.message.edit_text(
        'Вот ваши темы:'
    )
    for topic in all_topic:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Имя: {topic[1]}\n'
                 f'Сложность: {topic[3]}\n'
                 f'Количество задач: {len(topic[2].split("*"))}\n',
            reply_markup=KB.more_info(topic[0])
        )
        await asyncio.sleep(1)
    await call.message.answer(
        'Это все темы',
        reply_markup=KB.back_main()
    )
    await state.clear()


@router.callback_query(KB.Notices.filter(F.action == 'more_info'))
async def choose_difficulty(call: types.CallbackQuery, callback_data: KB.choose_dif):
    con = DB.Bot_connection()
    data = con.get_collection_info(callback_data.data)
    await call.message.edit_text(
        'Вот ваши темы:',
        reply_markup=KB.back_main()
    )
    for item in data[2].split("*"):
        item_info = con.get_topic_info(id=item)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Имя: {item_info[1]}\n'
                 f'Номер задачи: {item_info[2]}\n'
                 f'Выполнений: {item_info[3]}\n'
                 f'Тема: {item_info[4]}\n'
                 f'Сложность: {item_info[5]}\n',
            reply_markup=KB.link(item_info[-2])
        )
    await call.message.answer(
        'Это все темы!',
        reply_markup=KB.back_main()
    )
