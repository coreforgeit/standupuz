import gspread
from gspread.exceptions import WorksheetNotFound
from gspread.exceptions import APIError
from time import sleep

import db
from config import Config
from init import log_error


# проверка обновлений
def add_new_order_in_table(
        count_place: int,
        option: str,
        name: str,
        phone: str,
        page_id: int,
        order_id: int,
        username: str
) -> None:
    gc = gspread.service_account(filename=Config.google_key_path)
    table = gc.open_by_key(Config.google_table_id)
    page = table.get_worksheet_by_id(page_id)
    client_table = page.get(f'C11:C200')

    empty_row_index = len(client_table) + 11
    for i, row in enumerate(client_table):
        if row == ['-'] or row == []:
            empty_row_index = i + 11  # Прибавляем 10, чтобы получить номер строки в таблице
            break

    if not username:
        username = ''
        link = f'https://t.me/+{phone}'
    else:
        link = f'https://t.me/{username}'
        username = f'@{username}'

    row = [[order_id, count_place, option, name, username, phone, link]]
    cell = f'C{empty_row_index}:I{empty_row_index}'
    sleep(1)
    page.update(cell, row)
    # вернуть если формула будет криво работать
    # sleep(1)
    # page.update(option_count_cell, empty_place)