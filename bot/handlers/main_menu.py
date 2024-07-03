from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

import re
import asyncio

import db
import keyboards as kb
from config import Config
from init import dp, bot

from utils.base_utils import is_admin
from utils.entities_utils import recover_entities
from enums import BaseCB


# команда старт
@dp.message(CommandStart())
async def com_start(msg: Message, state: FSMContext):
    await state.clear()
    await db.add_user(user_id=msg.from_user.id, full_name=msg.from_user.full_name, username=msg.from_user.username)
    # admin_status = await is_admin(msg.from_user.id)
    admin_status = False
    # admin_status = True if msg.from_user.id == 524275902 else False
    if admin_status:
        text = '<b>Действия администратора:</b>'
        await msg.answer(text, reply_markup=kb.get_admin_kb())
    else:
        info = await db.get_info()
        events = await db.get_events(active=True)
        await msg.answer(
            text=info.hello_text,
            entities=recover_entities(info.hello_entities),
            parse_mode=None,
            reply_markup=kb.get_events_list_kb(events)
        )


# Вернуть первый экран
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.BACK_COM_START.value))
async def back_com_start(cb: CallbackQuery):
    info = await db.get_info()
    events = await db.get_events(active=True)
    await cb.message.edit_text(
        text=info.hello_text,
        entities=recover_entities(info.hello_entities),
        parse_mode=None,
        reply_markup=kb.get_events_list_kb(events)
    )


# Ссылки на соцсети
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.SOCIAL_MEDIAS.value))
async def social_medias(cb: CallbackQuery):
    text = f'Наши соцсети'
    await cb.message.edit_text(text, reply_markup=kb.get_social_medias_kb())


# Отмена
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.CLOSE.value))
async def social_medias(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.clear()
