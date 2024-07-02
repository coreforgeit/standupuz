from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from enums import AdminCB, BaseCB, Actions


# основная клавиатура админов
def get_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔄 Обновить таблицу', callback_data=AdminCB.UPDATE_TABLE.value)
    kb.button(text='➕ Создать ивент', callback_data=f'{AdminCB.NEW_EVENT.value}:{Actions.NEW.value}')
    kb.button(text='🖍 Изменить ивент', callback_data=AdminCB.EDIT_EVENT_LIST.value)
    kb.button(text='📲 Сделать рассылку', callback_data=AdminCB.SEND_MESSAGE_1.value)
    kb.button(text='🙋‍♂️ Текст приветствия', callback_data=AdminCB.EDIT_HELLO_TEXT_1.value)
    kb.button(text='🚶 Войти как пользователь', callback_data=BaseCB.BACK_COM_START.value)

    return kb.adjust(1).as_markup()
