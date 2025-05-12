from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.content_type import ContentType
from aiogram.enums.message_entity_type import MessageEntityType
from asyncio import sleep
from datetime import datetime

import re

import db
import keyboards as kb
import utils
from settings import conf, log_error
from init import client_router, bot
import utils as ut
from enums import AdminStatus, Action, AdminCB, EditEventStep


# основная функция изменений https://ticketon.uz/tashkent/event/stendap-otkrytyy-mikrofon-uz
async def edit_event(state: FSMContext, chat_id=None):
    await state.set_state(AdminStatus.CREATE_EVENT)
    data = await state.get_data()

    if conf.debug:
        for k, v in data.items():
            print(f'{k}: {v}')

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
               f'🔗 Ссылка: {data["ticket_url"]}\n' \
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
@client_router.callback_query(lambda cb: cb.data.startswith(AdminCB.BACK_EDIT_EVENT.value))
async def back_edit_event(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await cb.message.edit_reply_markup(reply_markup=kb.get_edit_event_kb(data['type']))


# начало создания
@client_router.callback_query(lambda cb: cb.data.startswith(AdminCB.NEW_EVENT.value))
async def create_new_event(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    _, action, event_id_str = cb.data.split(':')
    event_id = int(event_id_str)

    if action == Action.NEW.value:
        # if conf.debug:
        #     photo_id = 'AgACAgIAAxkBAAIZ_2gUuLrNeqcp3rrc4EVFQ4TqQ6xeAAI58DEbRdSpSOA0drmJIeU3AQADAgADeAADNgQ'
        # else:
        #     photo_id = 'AgACAgIAAxkBAAMDZJLz5wR0skvRu9z8XLdrFaYsz80AAvzOMRuk6phIPY914z_9bZoBAAMCAANtAAMvBA'
        await state.update_data(data={
            'is_first': True,
            'photo_id': conf.photo_default,
            'text': 'Добавьте текст',
            'title': '',
            'entities': [],
            'date': '',
            'time': '',
            'tariffs': [],
            'type': action,
            'club': '',
            'ticket_url': '',
        })

    elif action == Action.EDIT.value:
        event_info = await db.Event.get_event(event_id=event_id)
        entities = ut.recover_entities(event_info.entities)
        await state.update_data(data={
            'is_first': True,
            'photo_id': event_info.photo_id,
            'text': event_info.text,
            'title': '',
            'entities': entities,
            'date': '',
            'time': '',
            'tariffs': [],
            'type': action,
            'club': '',
            'event_id': event_id,
            'is_active': event_info.is_active,
            'ticket_url': event_info.ticket_url,
        })

    await edit_event(state, chat_id=cb.message.chat.id)


# принимает дату текстом
@client_router.message(StateFilter(AdminStatus.CREATE_EVENT))
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
@client_router.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_EVENT_1.value))
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
        pop_time = await db.Event.get_popular_time_list()
        await cb.answer('🖍 Изменить время')
        await cb.message.edit_reply_markup(reply_markup=kb.get_choice_time_kb(pop_time))

    elif step == EditEventStep.PRICE.value:
        await cb.answer('🖍 Места и опции')
        await cb.message.edit_reply_markup(reply_markup=kb.get_back_edit_event_kb())


# принимает текст сообщения
@client_router.message(StateFilter(AdminStatus.EDIT_EVENT))
async def edit_text(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()

    try:
        if data['step'] == EditEventStep.TITLE.value:
            await state.update_data(data={'title': msg.text})

        elif data['step'] == EditEventStep.CLUB.value:
            await state.update_data(data={'club': msg.text})

        elif data['step'] == EditEventStep.DATE.value:
            date = ut.hand_date(msg.text)
            if date == 'error':
                sent = await msg.answer('❌ Некорректный формат даты')
                await sleep(3)
                await sent.delete()
                return

            else:
                await state.update_data(data={'date': date})

        elif data['step'] == EditEventStep.TIME.value:
            time = ut.hand_time(msg.text)
            if time == 'error':
                sent = await msg.answer('❌ Некорректный формат времени')
                await sleep(3)
                await sent.delete()
                return

            else:
                await state.update_data(data={'time': time})

        elif data['step'] == EditEventStep.PRICE.value:
            if msg.entities and msg.entities[0].type == MessageEntityType.URL.value:
                await state.update_data(data={'ticket_url': msg.text})

            else:
                tariffs = []
                tariff_list = msg.text.split(',')
                for tariff in tariff_list:
                    print(tariff)
                    tariff_info = tariff.strip().split(' ')
                    place = int(tariff_info[0]) if tariff_info[0].isdigit() else 0
                    price = int(tariff_info[1]) if tariff_info[1].isdigit() else 0
                    if price < 10000:
                        price *= 1000
                    text = re.sub(r'\d+', '', tariff).strip().capitalize()
                    tariffs.append({'place': place, 'price': price, 'text': text})

                await state.update_data(data={'tariffs': tariffs})

    except Exception as e:
        log_error(e)

    await edit_event(state)


# принимает колбек с датой
@client_router.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_EVENT_2.value))
async def edit_event_2(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data['step'] == EditEventStep.DATE.value:
        _, date = cb.data.split(':')
        date = ut.hand_date(date)
        await state.update_data(data={'date': date})

    elif data['step'] == EditEventStep.TIME.value:
        _, time = cb.data.split(' ')  # есть двоеточие во времени
        await state.update_data(data={'time': time})

    await edit_event(state)


# подтвердить
@client_router.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_EVENT_ACCEPT.value))
async def create_new_event(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:

        if data['type'] == Action.NEW.value:

            if data['title'] == '':
                await cb.answer('❗️Ошибка. Добавьте название', show_alert=True)
                return

            if not data['tariffs'] and not data['ticket_url']:
                await cb.answer('❗️Ошибка. Добавьте опции', show_alert=True)
                return

            page_id = await ut.create_new_page(
                date=data['date'],
                time=data['time'],
                tariffs=data.get('tariffs'),
                title=data['title'],
                ticket_url=data['ticket_url'],
            )
            if not page_id:
                await cb.answer(
                    '❗️Ошибка. Вкладка с таким названием уже существует. Удалите старую вкладку или переименуйте '
                    'ивент', show_alert=True)
                return

            await state.clear()
            event_id = await db.Event.add_event(
                title=data['title'],
                club=data.get('club'),
                event_date=datetime.strptime(data['date'], conf.date_form).date(),
                event_time=datetime.strptime(data['time'], conf.time_form).time(),
                text=data['text'],
                entities=ut.save_entities(data['entities']),
                photo_id=data['photo_id'],
                ticket_url=data['ticket_url'],
                page_id=page_id,
                is_active=True,
            )

            # сохраняем фото для сайта
            await ut.save_photo(data['photo_id'], event_id)
            row_number = 5
            for option in data['tariffs']:
                await db.Option.add_option(
                    event_id=event_id,
                    name=option['text'],
                    empty_place=option['place'],
                    all_place=option['place'],
                    cell=f'B{row_number}',
                    price=option['price']
                )
                row_number += 1

            await cb.message.edit_reply_markup(reply_markup=kb.update_is_active_event_kb(True, event_id))

        else:
            await db.Event.update_event(
                event_id=data['event_id'],
                photo_id=data['photo_id'],
                text=data['text'],
                entities=ut.save_entities(data['entities']),
            )
            await ut.save_photo(data['photo_id'], data['event_id'])

            await cb.message.edit_reply_markup(
                reply_markup=kb.update_is_active_event_kb(data['is_active'], data['event_id']))

    except Exception as e:
        await cb.message.answer(f'❌ Не удалось сохранить\n{e}')


# изменить статус ивента
@client_router.callback_query(lambda cb: cb.data.startswith(AdminCB.EVENT_ACTIVE_STATUS.value))
async def event_active_status(cb: CallbackQuery):
    _, new_state_str, event_id_str = cb.data.split(':')
    new_state = bool(int(new_state_str))
    event_id = int(event_id_str)

    await db.Event.update_event(event_id=event_id, is_active=new_state)
    await cb.message.edit_reply_markup(reply_markup=kb.update_is_active_event_kb(new_state, event_id))
