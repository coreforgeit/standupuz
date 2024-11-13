from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import db
import keyboards as kb
from init import dp, bot
from utils.google_utils import google_update
from enums import AdminCB, AdminStatus


# вернуться к админ панели
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.BACK_START.value))
async def as_user(cb: CallbackQuery):
    text = '<b>Действия администратора:</b>'
    await cb.message.edit_text(text, reply_markup=kb.get_admin_kb())


# список ивентов для изменения
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_EVENT_LIST.value))
async def send_message_1(cb: CallbackQuery, state: FSMContext):
    text = '<b>Изменить ивент</b>'

    events = await db.get_events(last_10=True)
    await cb.message.edit_text(text, reply_markup=kb.get_10_last_event_kb(events))


# показывает текст, предлагает поменять
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_HELLO_TEXT_1.value))
async def edit_hello_text_1(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStatus.EDIT_HELLO_TEXT)

    info = await db.get_info()
    sent = await cb.message.answer(
        text=info.hello_text,
        parse_mode=None,
        reply_markup=kb.get_edit_hello_text_kb()
        )
    await state.update_data(data={'message_id': sent.message_id})


# команда старт
@dp.message(StateFilter(AdminStatus.EDIT_HELLO_TEXT))
async def edit_hello_text_2(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    await bot.edit_message_text(
        text=msg.text,
        chat_id=msg.chat.id,
        message_id=data['message_id'],
        entities=msg.entities,
        parse_mode=None,
        reply_markup=kb.get_edit_hello_text_kb()
    )


# показывает текст, предлагает поменять
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.EDIT_HELLO_TEXT_3.value))
async def edit_hello_text_3(cb: CallbackQuery, state: FSMContext):
    await state.clear()

    await db.update_info(hello_text=cb.message.text, hello_entities=cb.message.entities)
    await cb.message.edit_reply_markup(reply_markup=None)
    await cb.answer('✅ Текст успешно обновлён')


# Обновляет таблицу
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.UPDATE_TABLE.value))
async def update_google_table(cb: CallbackQuery, state: FSMContext):
    sent = await cb.message.answer('⏳')

    error_text = await google_update()
    if len(error_text) == 0:
        text = '✅ База обновлена'
    else:
        text = (f'‼️ База обновлена некорректно.\n'
                f'Ошибки:\n'
                f'{error_text}')

    await sent.edit_text(text=text[:4000])
