from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.content_type import ContentType
from asyncio import sleep
from datetime import datetime

import re

import db
import keyboards as kb
from config import Config, DEBUG
from init import dp, bot
from utils.base_utils import hand_date, hand_time
from utils.entities_utils import recover_entities, save_entities
from utils.google_utils import create_new_page
from enums import AdminStatus, Action, AdminCB, EditEventStep


# основная функция изменений
async def edit_event(state: FSMContext, chat_id=None):
    await state.set_state(AdminStatus.CREATE_EVENT)
    data = await state.get_data()

    tariff_text = ''
    for tariff in data['tariffs']:
        price_str = f'{tariff["price"]} UZS' if tariff["price"] else ''
        tariff_text += f'{tariff["place"]} - {tariff["text"]} {price_str}\n'

    if data['type'] == Action.NEW.value:
        text = f'{data["text"]}\n\n' \
               f'==============\n' \
               f'Название: {data["title"]}\n' \
               f'📍 Локация: {data["club"]}\n' \
               f'📅 Дата: {data["date"]}\n' \
               f'⏰ Время: {data["time"]}\n' \
               f'🫰 Места:\n{tariff_text}'

    else:
        text = data["text"]

    if data['is_first']:
        sent = await bot.send_photo(
            chat_id=chat_id,
            photo=data['photo_id'],
            caption=text,
            caption_entities=data['entities'],
            parse_mode=None,
            reply_markup=kb.get_edit_event_kb(data['type'])
        )

        await state.update_data(data={'is_first': False, 'chat_id': sent.chat.id, 'message_id': sent.message_id})
    else:
        photo = InputMediaPhoto(
            media=data['photo_id'], caption=text, caption_entities=data['entities'], parse_mode=None
        )
        await bot.edit_message_media(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            media=photo,
            reply_markup=kb.get_edit_event_kb(data['type'])
        )


# возвращает к
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.BACK_EDIT_EVENT.value))
async def back_edit_event(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await cb.message.edit_reply_markup(reply_markup=kb.get_edit_event_kb(data['type']))


# начало создания
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.NEW_EVENT.value))
async def create_new_event(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    _, action, event_id_str = cb.data.split(':')
    event_id = int(event_id_str)

    if action == Action.NEW.value:
        if DEBUG:
            photo_id = 'AgACAgIAAxkBAAILkWaGTBTmNF5imYbl7qomolVeK-5GAAIe1TEbUf84SDNLPE4RuP-eAQADAgADeAADNQQ'
        else:
            photo_id = 'AgACAgIAAxkBAAMDZJLz5wR0skvRu9z8XLdrFaYsz80AAvzOMRuk6phIPY914z_9bZoBAAMCAANtAAMvBA'
        await state.update_data(data={
            'is_first': True,
            'photo_id': photo_id,
            'text': 'Добавьте текст',
            'title': '',
            'entities': [],
            'date': '',
            'time': '',
            'tariffs': [],
            'type': 'new',
            'club': '',
        })

    elif action == Action.EDIT.value:
        event_info = await db.get_event(event_id=event_id)
        entities = await recover_entities(event_id=event_id)
        await state.update_data(data={
            'is_first': True,
            'photo_id': event_info.photo_id,
            'text': event_info.text,
            'title': '',
            'entities': entities,
            'date': '',
            'time': '',
            'tariffs': [],
            'type': 'edit',
            'club': '',
            'event_id': event_id,
            'is_active': event_info.is_active
        })

    await edit_event(state, chat_id=cb.message.chat.id)


# принимает дату текстом
@dp.message(StateFilter(AdminStatus.CREATE_EVENT))
async def edit_text(msg: Message, state: FSMContext):
    await msg.delete()

    if msg.content_type == ContentType.PHOTO:
        if not msg.caption:
            await state.update_data(data={
                'photo_id': msg.photo[-1].file_id
            })
        else:
            await state.update_data(data={
                'photo_id': msg.photo[-1].file_id,
                'text': msg.caption,
                'entities': msg.caption_entities
            })
    elif msg.content_type == ContentType.TEXT:
        await state.update_data(data={
            'text': msg.text,
            'entities': msg.entities
        })

    await edit_event(state)


# ==================================================================
# распределяет изменения, даёт статусы
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_EVENT_1.value))
async def create_new_event(cb: CallbackQuery, state: FSMContext):
    _, step = cb.data.split(':')
    await state.set_state(AdminStatus.EDIT_EVENT)
    await state.update_data(data={'step': step})
    if step == EditEventStep.TITLE.value:
        await cb.answer('🖍 Изменить название')
        await cb.message.edit_reply_markup(reply_markup=kb.get_back_edit_event_kb())

    if step == EditEventStep.CLUB.value:
        await cb.answer('🖍 Изменить локацию')
        await cb.message.edit_reply_markup(reply_markup=kb.get_back_edit_event_kb())

    elif step == EditEventStep.DATE.value:
        await cb.answer('🖍 Изменить дату')
        await cb.message.edit_reply_markup(reply_markup=kb.get_choice_date_kb())

    elif step == EditEventStep.TIME.value:
        pop_time = await db.get_popular_time_list()
        await cb.answer('🖍 Изменить время')
        await cb.message.edit_reply_markup(reply_markup=kb.get_choice_time_kb(pop_time))

    elif step == EditEventStep.PRICE.value:
        await cb.answer('🖍 Места и опции')
        await cb.message.edit_reply_markup(reply_markup=kb.get_back_edit_event_kb())


# принимает текст сообщения
@dp.message(StateFilter(AdminStatus.EDIT_EVENT))
async def edit_text(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()

    if data['step'] == EditEventStep.TITLE.value:
        await state.update_data(data={'title': msg.text})

    elif data['step'] == EditEventStep.CLUB.value:
        await state.update_data(data={'club': msg.text})

    elif data['step'] == EditEventStep.DATE.value:
        date = hand_date(msg.text)
        if date == 'error':
            sent = await msg.answer('❌ Некорректный формат даты')
            await sleep(3)
            await sent.delete()
            return

        else:
            await state.update_data(data={'date': date})

    elif data['step'] == EditEventStep.TIME.value:
        time = hand_time(msg.text)
        if time == 'error':
            sent = await msg.answer('❌ Некорректный формат времени')
            await sleep(3)
            await sent.delete()
            return

        else:
            await state.update_data(data={'time': time})

    elif data['step'] == EditEventStep.PRICE.value:
        tariffs = []
        tariff_list = msg.text.split(',')
        for tariff in tariff_list:
            tariff_info = tariff.strip().split(' ')
            place = int(tariff_info[0]) if tariff_info[0].isdigit() else 0
            price = int(tariff_info[1]) if tariff_info[1].isdigit() else 0
            if price < 10000:
                price *= 1000
            text = re.sub(r'\d+', '', tariff).strip().capitalize()
            tariffs.append({'place': place, 'price': price, 'text': text})

        await state.update_data(data={'tariffs': tariffs})

    await edit_event(state)


# принимает колбек с датой
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_EVENT_2.value))
async def edit_event_2(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data['step'] == EditEventStep.DATE.value:
        _, date = cb.data.split(':')
        date = hand_date(date)
        await state.update_data(data={'date': date})

    elif data['step'] == EditEventStep.TIME.value:
        _, time = cb.data.split(' ')  # есть двоеточие во времени
        await state.update_data(data={'time': time})

    await edit_event(state)


# подтвердить
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_EVENT_ACCEPT.value))
async def create_new_event(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data['type'] == Action.NEW.value:

        if data['title'] == '':
            await cb.answer('❗️Ошибка. Добавьте название', show_alert=True)
            return

        if not data['tariffs']:
            await cb.answer('❗️Ошибка. Добавьте опции', show_alert=True)
            return

        page_id = await create_new_page(data['date'], data['time'], data['tariffs'], data['title'])
        if not page_id:
            await cb.answer(
                '❗️Ошибка. Вкладка с таким названием уже существует. Удалите старую вкладку или переименуйте '
                'ивент', show_alert=True)
        else:
            await state.clear()
            event_id = await db.add_event(
                title=data['title'],
                club=data.get('club'),
                event_date=datetime.strptime(data['date'], Config.date_form).date(),
                event_time=datetime.strptime(data['time'], Config.time_form).time(),
                text=data['text'],
                photo_id=data['photo_id'],
                page_id=page_id,
                is_active=True,
            )
            await save_entities(event_id=event_id, entities=data['entities'])

            # tariffs.append({'place': place, 'price': price, 'text': text})
            row_number = 5
            for option in data['tariffs']:
                await db.add_option(
                    event_id=event_id,
                    title=option['text'],
                    empty_place=option['place'],
                    all_place=option['place'],
                    cell=f'B{row_number}',
                    price=option['price']
                )
                row_number += 1

            await cb.message.edit_reply_markup(reply_markup=kb.update_is_active_event_kb(True, event_id))

    else:
        await db.update_event(
            event_id=data['event_id'],
            photo_id=data['photo_id'],
            text=data['text'],
            # entities=save_entities(data['entities']),
        )
        await save_entities(event_id=data['event_id'], entities=data['entities'])
        await cb.message.edit_reply_markup(
            reply_markup=kb.update_is_active_event_kb(data['is_active'], data['event_id']))


# изменить статус ивента
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.EVENT_ACTIVE_STATUS.value))
async def event_active_status(cb: CallbackQuery):
    _, new_state_str, event_id_str = cb.data.split(':')
    new_state = bool(int(new_state_str))
    event_id = int(event_id_str)

    await db.update_event(event_id=event_id, is_active=new_state)
    await cb.message.edit_reply_markup(reply_markup=kb.update_is_active_event_kb(new_state, event_id))
