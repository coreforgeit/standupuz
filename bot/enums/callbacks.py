from enum import Enum


class BaseCB(str, Enum):
    BACK_COM_START = 'back_com_start'
    SOCIAL_MEDIAS = 'social_medias'
    CLOSE = 'close'


class AdminCB(str, Enum):
    BACK_START = 'back_admin_start'
    BACK_EDIT_EVENT = 'back_edit_event'
    UPDATE_TABLE = 'update_google_table'
    NEW_EVENT = 'new_event'
    EDIT_EVENT_LIST = 'edit_event_list'
    EDIT_EVENT_1 = 'edit_event_step_1'
    EDIT_EVENT_2 = 'edit_event_step_2'
    EVENT_ACTIVE_STATUS = 'event_active_status'
    EDIT_EVENT_ACCEPT = 'edit_event_accept'
    EDIT_HELLO_TEXT_1 = 'edit_hello_text_1'
    EDIT_HELLO_TEXT_3 = 'edit_hello_text_3'
    SEND_MESSAGE_1 = 'send_message_1'
    SEND_MESSAGE_2 = 'send_message_2'
    SEND_MESSAGE_3 = 'send_message_3'
    SEND_MESSAGE_4 = 'send_message_4'


class UserCB(str, Enum):
    VIEW_EVENT = 'view_event'
    BOOK_1 = 'book_1'
    BOOK_2 = 'book_2'
    BOOK_3 = 'book_3'
    BOOK_4 = 'book_4'
    BOOK_5 = 'book_5'
    BOOK_6 = 'book_6'
