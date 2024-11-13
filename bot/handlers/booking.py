from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import re
import asyncio

import db
import keyboards as kb
from init import dp, bot

from utils.message_utils import send_event, end_book
from enums import UserCB, UserStatus


# показывает ивент
@dp.callback_query(lambda cb: cb.data.startswith(UserCB.VIEW_EVENT.value))
async def view_event(cb: CallbackQuery):
    _, event_id_str = cb.data.split(':')
    event_id = int(event_id_str)

    await send_event(event_id=event_id, user_id=cb.from_user.id)


# показывает ивент
@dp.callback_query(lambda cb: cb.data.startswith(UserCB.BOOK_1.value))
async def book_1(cb: CallbackQuery, state: FSMContext):
    event_id, option_id = map(int, cb.data.split(':')[1:])

    if not option_id:
        await cb.answer('Свободные места закончились', show_alert=True)
        return

    info = await db.get_info()
    if not event_id:
        data = await state.get_data()
        event_info = await db.get_event(data['event_id'])
        text = event_info.text_1 if event_info.text_1 else info.text_1
        await cb.message.edit_text(text, reply_markup=kb.get_alert_kb(1))
    else:
        event_info = await db.get_event(event_id)
        await state.set_state(UserStatus.CHOICE_COUNT_PLACE)

        text = event_info.text_1 if event_info.text_1 else info.text_1
        sent = await cb.message.answer(text,  reply_markup=kb.get_alert_kb(1))
        await state.update_data(data={
            'chat_id': sent.chat.id,
            'message_id': sent.message_id,
            'event_id': event_id,
            'option_id': option_id,
            'user_id': cb.from_user.id,
            'username': cb.from_user.username,
            'page_id': event_info.page_id,
            'event_title': event_info.title
        })


# второй текст предупреждение
@dp.callback_query(lambda cb: cb.data.startswith(UserCB.BOOK_2.value))
async def book_2(cb: CallbackQuery, state: FSMContext):
    info = await db.get_info()
    data = await state.get_data()

    event_info = await db.get_event(data['event_id'])
    text = event_info.text_2 if event_info.text_2 else info.text_2

    await cb.message.edit_text(text, reply_markup=kb.get_alert_kb(2))


# количество мест
@dp.callback_query(lambda cb: cb.data.startswith(UserCB.BOOK_3.value))
async def book_3(cb: CallbackQuery, state: FSMContext):
    text = 'Укажите количество мест (или введите число)'
    await cb.message.edit_text(text, reply_markup=kb.get_select_count_place_kb())


# запись количества мест  ===============================================================
async def book_4(count_free_place: int, user_id: int, state: FSMContext):
    data = await state.get_data()
    option_info = await db.get_option(data['option_id'])

    if option_info.empty_place < count_free_place:
        sent = await bot.send_message(chat_id=user_id, text=f'Осталось только {option_info.empty_place} мест')
        await asyncio.sleep(5)
        await sent.delete()

    else:
        await state.update_data(data={'count_place': count_free_place})

        user_info = await db.get_user_info(user_id)
        await state.set_state(UserStatus.SEND_CONTACT)
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=data['message_id'],
            text='Укажите контактный телефон',
            reply_markup=kb.get_sent_phone_kb(user_info.phone)
        )


# принимает количество мест цифрой
@dp.message(StateFilter(UserStatus.CHOICE_COUNT_PLACE))
async def book_4_text(msg: Message, state: FSMContext):
    await msg.delete()

    count_free_place = int(re.sub(r"[^\d,]", "", msg.text) or 0)
    await book_4(count_free_place=count_free_place, user_id=msg.chat.id, state=state)


# принимает количество мест колбеком
@dp.callback_query(lambda cb: cb.data.startswith(UserCB.BOOK_4.value))
async def book_4_cb(cb: CallbackQuery, state: FSMContext):
    _, count_place_str = cb.data.split(':')
    if count_place_str == 'back':
        data = await state.get_data()
        count_place_str = data['count_place']

    await book_4(count_free_place=int(count_place_str), user_id=cb.message.chat.id, state=state)


# запись телефон  ===============================================================
async def book_5(phone: str, user_id: int, first_name: str,  state: FSMContext):
    await db.update_user_info(user_id=user_id, phone=phone)
    await state.update_data(data={'phone': phone})
    data = await state.get_data()

    await state.set_state(UserStatus.SEND_NAME)
    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['message_id'],
        text='Укажите имя',
        reply_markup=kb.get_sent_name_kb(first_name),
        )


# принимает телефон цифрой
@dp.message(StateFilter(UserStatus.SEND_CONTACT))
async def book_5_text(msg: Message, state: FSMContext):
    await msg.delete()

    phone = msg.contact.phone_number if msg.contact else msg.text
    if not phone:
        sent = await msg.answer('❗️ Некорректный номер')
        await asyncio.sleep(5)
        await sent.delete()
        return

    await book_5(phone=phone, user_id=msg.from_user.id, first_name=msg.from_user.first_name, state=state)


# принимает телефон калбеком
@dp.callback_query(lambda cb: cb.data.startswith(UserCB.BOOK_5.value))
async def book_5_cb(cb: CallbackQuery, state: FSMContext):
    _, phone = cb.data.split(':')

    await book_5(phone=phone, user_id=cb.from_user.id, first_name=cb.from_user.first_name, state=state)


# запись телефон  ===============================================================
async def book_6(user_id: int, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    event_info = await db.get_event(data['event_id'])

    text = event_info.text_3
    if not text:
        info = await db.get_info()
        text = info.text_3

    await bot.edit_message_text(text=text, chat_id=user_id, message_id=data['message_id'])

    await end_book(data)


# Принимает имя текстом
@dp.message(StateFilter(UserStatus.SEND_NAME))
async def book_6_text(msg: Message, state: FSMContext):
    await msg.delete()
    await state.update_data(data={'name': msg.text.capitalize()})
    await book_6(user_id=msg.from_user.id, state=state)


# принимает телефон калбеком
@dp.callback_query(lambda cb: cb.data.startswith(UserCB.BOOK_6.value))
async def book_6_cb(cb: CallbackQuery, state: FSMContext):
    _, name = cb.data.split(':')
    await state.update_data(data={'name': name})

    await book_6(user_id=cb.from_user.id, state=state)
