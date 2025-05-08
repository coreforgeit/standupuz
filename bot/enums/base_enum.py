from enum import Enum


# Команды меню
class MenuCommand(Enum):
    START = ('start', 'Перезапуск 🚀')

    def __init__(self, command, label):
        self.command = command
        self.label = label


class Action(str, Enum):
    NEW = 'new'
    BACK = 'back'
    EDIT = 'edit'
    EVERYONE = 'everyone'


class EditEventStep(str, Enum):
    TITLE = 'title'
    CLUB = 'club'
    DATE = 'date'
    TIME = 'time'
    PRICE = 'price'


class Key(str, Enum):
    CLOSE_EVENT = 'close_event'

