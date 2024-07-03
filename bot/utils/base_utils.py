from datetime import datetime, timedelta
import asyncio

import db
from init import bot, log_error
from config import Config
from utils.google_utils import add_new_order_in_table


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

    if len(date_list) == 1:
        today = datetime.now(Config.tz)
        if int(date_list[0]) > today.day:
            # date = f'{date_list[0]}.{today.month}.{today.year}'
            date = f'{date_list[0]}.{today.month}'
        else:
            month = today.month + 1 if today.month < 12 else 1
            # year = today.year if month != 1 else today.year + 1
            # date = f'{date_list[0]}.{month}.{year}'
            date = f'{date_list[0]}.{month}'

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


# добавляет пользователя в таблицу
async def end_book(data: dict):
    # запись в таблицу, запись в базу, оповещение
    await db.update_option(option_id=data['option_id'], edit_place=0 - data['count_place'])
    option_info = await db.get_option(option_id=data['option_id'])
    order_id = await db.add_order(
        user_id=data['user_id'],
        phone=data['phone'],
        event_id=data['event_id'],
        option=option_info.name,
        count_place=data['count_place'],
        page_id=data['page_id'])

    in_table = False
    i = 0
    while in_table is False:
        try:
            add_new_order_in_table(
                count_place=data['count_place'],
                option=option_info.name,
                name=data['name'],
                phone=data['phone'],
                page_id=data['page_id'],
                order_id=order_id,
                username=data['username']
            )
            in_table = True
            await db.update_order(order_id=order_id, in_google=True)
            text = f'Новая бронь:\n' \
                   f'{option_info.name} - {data["count_place"]}\n' \
                   f'{data["event_title"]}\n' \
                   f'{data["name"]}\n' \
                   f'{data["phone"]}\n'

            await bot.send_message(Config.admin_group_id, text)

        except Exception as ex:
            i += 1
            if i > 30:
                in_table = 'error'
                log_error(f'end try add row {i} {ex}', with_traceback=False)
                text = (f'‼️ ОШИБКА! Ваша бронь не была добавлена. Попробуйте ещё раз. Если ошибка будет повторяться, '
                        f'обратитесь в поддержку')
                await bot.send_message(data['user_id'], text)
            else:
                log_error(f'try add row {i} {ex}', with_traceback=False)
                await asyncio.sleep(5)