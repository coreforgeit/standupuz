from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.content_type import ContentType

import db
import keyboards as kb
from init import dp, bot, log_error
from enums import AdminCB, AdminStatus, Action


# Отправить сообщение
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.SEND_MESSAGE_1.value))
async def send_message_1(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStatus.SEND_MESSAGE)
    await state.update_data(data={'choice_list': [], 'everyone': False})
    await cb.answer('Отправьте сообщение для рассылки', show_alert=True)


# команда старт
@dp.message(StateFilter(AdminStatus.SEND_MESSAGE))
async def send_message_2(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    events = await db.get_events(last_10=True)

    await state.update_data(data={'events': events})
    keyboard = kb.get_send_message_kb(events=events, data=data)

    if msg.content_type == ContentType.TEXT:
        await msg.answer(msg.text, entities=msg.entities, reply_markup=keyboard)

    elif msg.content_type == ContentType.PHOTO:
        await msg.answer_photo(
            photo=msg.photo[-1].file_id,
            caption=msg.caption,
            caption_entities=msg.caption_entities,
            parse_mode=None,
            reply_markup=keyboard
        )
    elif msg.content_type == ContentType.VIDEO:
        await msg.answer_video(
            video=msg.video.file_id,
            caption=msg.caption,
            caption_entities=msg.caption_entities,
            parse_mode=None,
            reply_markup=keyboard
        )
    elif msg.content_type == ContentType.ANIMATION:
        await msg.answer_animation(
            animation=msg.animation.file_id,
            caption=msg.caption,
            caption_entities=msg.caption_entities,
            parse_mode=None,
            reply_markup=keyboard
        )


# Сменить клавиатуру
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.SEND_MESSAGE_3.value))
async def send_message_3(cb: CallbackQuery, state: FSMContext):
    _, action = cb.data.split(':')
    data = await state.get_data()

    if action == Action.EVERYONE:
        everyone = False if data['everyone'] else True
        await state.update_data(data={'everyone': everyone})
    else:
        choice_id = int(action)
        choice_list = data['choice_list']
        if choice_id in choice_list:
            choice_list.remove(choice_id)
        else:
            choice_list.append(choice_id)

        await state.update_data(data={'choice_list': choice_list, 'everyone': False})

    data = await state.get_data()
    await cb.message.edit_reply_markup(reply_markup=kb.get_send_message_kb(events=data['events'], data=data))


# Рассылка
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.SEND_MESSAGE_4.value))
async def send_message_4(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data == {}:
        await cb.answer('❕Данные устарели')
        return

    await state.clear()
    await cb.answer('⏳ Рассылка сообщений, может уйти некоторое время')
    sent = await cb.message.answer('⏳')

    if data['everyone']:
        users = await db.get_users()
        users_id = [user.user_id for user in users]
    else:
        orders = await db.get_users_for_mailing(data['choice_list'])
        users_id = [order.user_id for order in orders]

    counter = 0
    users_id = list(set(users_id))
    # users_id = [5772948261, 524275902]
    for user_id in users_id:
        try:
            if cb.message.content_type == ContentType.TEXT:
                await bot.send_message(
                    chat_id=user_id,
                    text=cb.message.text, entities=cb.message.entities,
                    parse_mode=None
                )
            elif cb.message.content_type == ContentType.PHOTO:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=cb.message.photo[-1].file_id,
                    caption=cb.message.caption,
                    caption_entities=cb.message.caption_entities,
                    parse_mode=None
                )
            elif cb.message.content_type == ContentType.VIDEO:
                await bot.send_video(
                    chat_id=user_id,
                    video=cb.message.video.file_id,
                    caption=cb.message.caption,
                    caption_entities=cb.message.caption_entities,
                    parse_mode=None
                )
            elif cb.message.content_type == ContentType.ANIMATION:
                await bot.send_animation(
                    chat_id=user_id,
                    animation=cb.message.animation.file_id,
                    aption=cb.message.caption,
                    caption_entities=cb.message.caption_entities,
                    parse_mode=None
                )
            counter += 1
        except Exception as ex:
            pass
            log_error(f'send message user {user_id} {ex}', with_traceback=False)

    await sent.edit_text(f'⌛️ Отправлено {counter} сообщений')
