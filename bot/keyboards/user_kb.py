from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from enums import UserCB, BaseCB, Action


# список ивентов
def get_events_list_kb(events: tuple[db.EventRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Узнать о Standup.uz', callback_data=BaseCB.SOCIAL_MEDIAS.value)
    if events:
        for event in events:
            kb.button(text=event.title, callback_data=f'{UserCB.VIEW_EVENT.value}:{event.id}')
    return kb.adjust(1).as_markup()


# ссылки на соцсети
def get_social_medias_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Instagram', url='https://instagram.com/standup.uz?igshid=ZDdkNTZiNTM=')
    kb.button(text='Telegram', url='https://t.me/StandUp_UZB')
    kb.button(text='YouTube', url='https://www.youtube.com/channel/UCtDA0xLMJ76jg0vmdk7FZdw')
    kb.button(text='🔙 Назад', callback_data=BaseCB.BACK_COM_START.value)
    return kb.adjust(1).as_markup()


# забронировать места
def get_book_kb(options: tuple[db.OptionRow], from_start: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if from_start:
        kb.button(text='🔙 Назад', callback_data=BaseCB.BACK_COM_START.value)
    else:
        kb.button(text='🔙 Назад', callback_data=BaseCB.CLOSE.value)
    for option in options:
        if option.empty_place > 0:
            caption = f'{option.name} ({option.empty_place})'
            kb.button(text=caption, callback_data=f'{UserCB.BOOK_1.value}:{option.event_id}:{option.id}')
        else:
            caption = f'{option.name} (Мест нет)'
            kb.button(text=caption, callback_data=f'{UserCB.BOOK_1.value}:{option.event_id}:0')

    return kb.adjust(1).as_markup()


# предупреждение перед бронью
def get_alert_kb(step: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if step == 1:
        kb.button(text='Принял, далее', callback_data=f'{UserCB.BOOK_2.value}:1')
        kb.button(text='🔙 Назад', callback_data=f'{BaseCB.CLOSE.value}')
    else:
        kb.button(text='Принял, далее', callback_data=f'{UserCB.BOOK_3.value}')
        kb.button(text='🔙 Назад', callback_data=f'{UserCB.BOOK_1.value}:0:1')
    return kb.adjust(1).as_markup()


# выбор свободных мест
def get_select_count_place_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i in [1, 2, 3, 4]:
        kb.button(text=f'{i}', callback_data=f'{UserCB.BOOK_4.value}:{i}')

    return kb.adjust(2).as_markup()


# подсказка в отправке телефона
def get_sent_phone_kb(phone: str = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if phone:
        kb.button(text=f'{phone}', callback_data=f'{UserCB.BOOK_5.value}:{phone}')
    kb.button(text='🔙 Назад', callback_data=f'{UserCB.BOOK_3.value}')

    return kb.adjust(1).as_markup()


# подсказка в отправке имени
def get_sent_name_kb(name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f'{name}', callback_data=f'{UserCB.BOOK_6.value}:{name}')
    kb.button(text='🔙 Назад', callback_data=f'{UserCB.BOOK_4.value}:{Action.BACK.value}')

    return kb.adjust(1).as_markup()
