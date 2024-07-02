from enum import Enum


class UserStatus(str, Enum):
    CHOICE_COUNT_PLACE = 'choice_count_place'
    SEND_CONTACT = 'send_contact'
    SEND_NAME = 'send_name'
