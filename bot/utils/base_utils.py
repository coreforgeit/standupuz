from datetime import datetime, timedelta

import db
from init import bot, log_error
from config import Config


# проверка на админа
async def is_admin(user_id):
    user = await bot.get_chat_member(Config.admin_group_id, user_id)
    if user.status == 'creator' or user.status == 'administrator':
        return True
    else:
        return False


# возвращает корректный формат даты
def hand_date(text: str) -> str:
    date = text.replace(' ', '.')
    date_list = text.split('.')
    today = datetime.now(Config.tz)
    if len(date_list) == 1:
        if int(date_list[0]) > today.day:
            month = f'0{today.month}' if today.month < 10 else today.month
            date = f'{date_list[0]}.{month}.{today.year}'
        else:
            month = today.month + 1 if today.month < 12 else 1
            year = today.year if month != 1 else today.year + 1
            date = f'{date_list[0]}.{month}.{year}'

    elif len(date_list) == 2:
        date = f'{date_list[0]}.{date_list[1]}.{today.year}'

    return date


# возвращает корректный формат времени
def hand_time(text: str):
    time = text.replace('.', ':').replace(' ', ':')
    time_list = text.split(':')

    if len(time_list) == 1:
        time = f'{time_list[0]}:00'

    try:
        datetime.strptime(time, "%H:%M").time()
        return time
    except Exception as ex:
        log_error(ex)
        return 'error'


# возвращает даты ближайших выходных
def get_weekend_date_list():
    date_list = []
    today = datetime.now(Config.tz).date()
    today_number = today.weekday()

    if today_number <= 4:
        add_day = 4 - today_number
    else:
        add_day = 6 if today_number == 5 else 5

    for i in range(0, 3):
        date = today + timedelta(days=add_day + i)
        date_list.append(date.strftime(Config.day_form))
    for i in range(7, 10):
        date = today + timedelta(days=add_day + i)
        date_list.append(date.strftime(Config.day_form))

    return date_list
