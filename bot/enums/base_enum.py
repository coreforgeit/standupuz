from enum import Enum


class Action(str, Enum):
    NEW = 'new'
    BACK = 'back'
    EDIT = 'edit'
    EVERYONE = 'everyone'


class EditEventStep(str, Enum):
    TITLE = 'title'
    DATE = 'date'
    TIME = 'time'
    PRICE = 'price'
