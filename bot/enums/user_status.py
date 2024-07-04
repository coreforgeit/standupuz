from enum import Enum


class UserStatus(str, Enum):
    CHOICE_COUNT_PLACE = 'choice_count_place'
    SEND_CONTACT = 'send_contact'
    SEND_NAME = 'send_name'


class AdminStatus(str, Enum):
    SEND_MESSAGE = 'send_message'
    EDIT_HELLO_TEXT = 'edit_hello_text'
    CREATE_EVENT = 'create_event'
    EDIT_EVENT = 'edit_event'
