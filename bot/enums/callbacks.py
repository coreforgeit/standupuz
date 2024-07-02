from enum import Enum


class BaseCB(str, Enum):
    BACK_COM_START = 'back_com_start'
    SOCIAL_MEDIAS = 'social_medias'
    CLOSE = 'close'


class AdminCB(str, Enum):
    UPDATE_TABLE = 'update_google_table'
    NEW_EVENT = 'new_event'
    EDIT_EVENT_LIST = 'edit_event_list'
    SEND_MESSAGE_1 = 'send_message_1'
    EDIT_HELLO_TEXT_1 = 'edit_hello_text_1'


class UserCB(str, Enum):
    VIEW_EVENT = 'view_event'
    BOOK_1 = 'book_1'
    BOOK_2 = 'book_2'
    BOOK_3 = 'book_3'
    BOOK_4 = 'book_4'
    BOOK_5 = 'book_5'
    BOOK_6 = 'book_6'
