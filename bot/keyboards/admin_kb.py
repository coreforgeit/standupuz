from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from config import Config
from utils.base_utils import get_weekend_date_list
from enums import AdminCB, BaseCB, Action, EditEventStep


# основная клавиатура админов
def get_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔄 Обновить таблицу', callback_data=AdminCB.UPDATE_TABLE.value)
    kb.button(text='➕ Создать ивент', callback_data=f'{AdminCB.NEW_EVENT.value}:{Action.NEW.value}:0')
    kb.button(text='🖍 Изменить ивент', callback_data=AdminCB.EDIT_EVENT_LIST.value)
    kb.button(text='📲 Сделать рассылку', callback_data=AdminCB.SEND_MESSAGE_1.value)
    kb.button(text='🙋‍♂️ Текст приветствия', callback_data=AdminCB.EDIT_HELLO_TEXT_1.value)
    kb.button(text='🚶 Войти как пользователь', callback_data=BaseCB.BACK_COM_START.value)

    return kb.adjust(1).as_markup()


# 10 последних ивентов
def get_10_last_event_kb(events: tuple[db.EventRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=AdminCB.BACK_START.value)

    for event in events:
        is_active = 'актив.' if event.is_active == 1 else 'не актив.'
        kb.button(
            text=f'{event.title} ({is_active})',
            callback_data=f'{AdminCB.NEW_EVENT.value}:{Action.EDIT.value}:{event.id}')

    return kb.adjust(1).as_markup()


# Отправка сообщений
def get_send_message_kb(events: tuple[db.EventRow], data: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=BaseCB.CLOSE.value)
    kb.button(
        text='✔️ Всем пользователям' if data['everyone'] else 'Всем пользователям',
        callback_data=f'{AdminCB.SEND_MESSAGE_3.value}:{Action.EVERYONE.value}'
    )
    for event in events:
        emoji = '✔️' if data['everyone'] or event.id in data['choice_list'] else ''
        kb.button(
            text=f'{emoji} {event.title} ({event.event_date})'.strip(),
            callback_data=f'{AdminCB.SEND_MESSAGE_3.value}:{event.id}'
        )
    kb.button(text='📲 Отправить', callback_data=AdminCB.SEND_MESSAGE_4.value)
    return kb.adjust(1).as_markup()


# изменение приветственного текста
def get_edit_hello_text_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=BaseCB.CLOSE.value)
    kb.button(text='✅ Подтвердить', callback_data=AdminCB.EDIT_HELLO_TEXT_3.value)
    return kb.adjust(1).as_markup()


# создать ивент
def get_edit_event_kb(type_event: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if type_event == Action.NEW.value:
        kb.button(text='🖍 Название', callback_data=f'{AdminCB.EDIT_EVENT_1.value}:{EditEventStep.TITLE.value}')
        kb.button(text='📍 Локация', callback_data=f'{AdminCB.EDIT_EVENT_1.value}:{EditEventStep.CLUB.value}')
        kb.button(text='📅 Дата', callback_data=f'{AdminCB.EDIT_EVENT_1.value}:{EditEventStep.DATE.value}')
        kb.button(text='⏰ Время', callback_data=f'{AdminCB.EDIT_EVENT_1.value}:{EditEventStep.TIME.value}')
        kb.button(text='🫰 Места и опции', callback_data=f'{AdminCB.EDIT_EVENT_1.value}:{EditEventStep.PRICE.value}')
        kb.button(text='✅ Создать', callback_data=f'{AdminCB.EDIT_EVENT_ACCEPT.value}')

    else:
        kb.button(text='✅ Подтвердить', callback_data=f'{AdminCB.EDIT_EVENT_ACCEPT.value}')

    return kb.adjust(2, 3, 1).as_markup()


# предлагает выбрать время
def get_choice_date_kb() -> InlineKeyboardMarkup:
    date_list = get_weekend_date_list()
    kb = InlineKeyboardBuilder()
    for date in date_list:
        kb.button(text=f'{date}', callback_data=f'{AdminCB.EDIT_EVENT_2.value}:{date}')

    kb.button(text='🔙 Назад', callback_data=AdminCB.BACK_EDIT_EVENT.value)
    return kb.adjust(2).as_markup()


# предлагает выбрать время
def get_choice_time_kb(times: tuple[db.PopTimeRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for time in times:
        time_str = time.event_time.strftime(Config.time_form)
        kb.button(text=time_str, callback_data=f'{AdminCB.EDIT_EVENT_2.value} {time_str}')

    kb.button(text='🔙 Назад', callback_data=AdminCB.BACK_EDIT_EVENT.value)
    return kb.adjust(2).as_markup()


# предлагает выбрать время
def get_back_edit_event_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=AdminCB.BACK_EDIT_EVENT.value)
    return kb.adjust(2).as_markup()


# переключение активный неактивный ивент
def update_is_active_event_kb(is_active: bool, event_id: int):
    kb = InlineKeyboardBuilder()
    if is_active:
        kb.button(text='✅ Активный', callback_data=f'{AdminCB.EVENT_ACTIVE_STATUS.value}:0:{event_id}')
    else:
        kb.button(text='❌ Неактивный', callback_data=f'{AdminCB.EVENT_ACTIVE_STATUS.value}:1:{event_id}')
    return kb.adjust(2).as_markup()
