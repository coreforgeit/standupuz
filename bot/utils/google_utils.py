import gspread
from gspread.exceptions import APIError
from gspread.utils import ValueRenderOption
from time import sleep
from datetime import datetime

import db
from config import Config
from init import log_error


# добавляет данные в таблицу
async def create_new_page(date: str, time: str, tariffs: list[dict], title: str) -> int:
    gc = gspread.service_account(filename=Config.google_key_path)
    table = gc.open_by_key(Config.google_table_id)
    # проверка таблицы
    try:
        page = table.add_worksheet(title=title, cols=20, rows=200)
    except APIError as ex:
        log_error(ex)
        return 0

    # Настройки
    setting_list = [['Активна', ''],
                    ['Название', title],
                    ['Дата', date],
                    ['Время', time]]

    option_row = 5
    for tariff in tariffs:
        formula = f'={tariff["place"]}-SUMIFS(D:D; E:E; A{option_row})'
        setting_list.append([tariff["text"], formula])
        option_row += 1
    page.update(range_name=f'a1:b10', values=setting_list, raw=False)

    # тексты
    info = await db.get_info()
    page.merge_cells('E1:J3')
    page.update(range_name='D1:1', values=[['Текст 1', info.text_1]])
    sleep(1)
    page.merge_cells('E4:J6')
    page.update(range_name='D4:E4', values=[['Текст 2', info.text_2]])
    sleep(1)
    page.merge_cells('E7:J9')
    page.update(range_name='D7:E7', values=[['Финальный текст', info.text_3]])
    sleep(1)

    # таблица гостей
    head_list = [['ID', 'Мест', 'Опции', 'Имя', 'Username', 'Телефон', 'Ссылка', 'Оплатил', 'Примечание', 'Откуда']]
    for i in range(0, 190):
        head_list.append(['', '', '-', '', '', '', '', '', '', ''])
    cells = f'c10:l200'
    page.update(range_name=cells, values=head_list)
    sleep(1)
    # триггер активности
    page.update(range_name='C1', values=[['S']])

    return page.id


async def google_update() -> str:
    error_text = ''
    gc = gspread.service_account (filename=Config.google_key_path)
    tables = gc.open_by_key (Config.google_table_id)

    # обновляем настройки
    try:
        base_text_1 = tables.sheet1.acell('E3').value
        base_text_2 = tables.sheet1.acell('E7').value
        base_text_3 = tables.sheet1.acell('E11').value

        await db.update_info(text_1=base_text_1, text_2=base_text_2, text_3=base_text_3)
    except Exception as ex:
        log_error(ex)
        error_text = f'{error_text}\n❌ Не удалось обновить базовые тексты:\n{ex}'

    active_events = await db.get_events(active=True)
    active_page_ids = [event.page_id for event in active_events]
    for table in tables:
        if table.id in active_page_ids:
            event = await db.get_event(page_id=table.id)
            # проверить тексты
            try:
                text_1 = table.acell('E1').value
                text_2 = table.acell('E4').value
                text_3 = table.acell('E7').value

                await db.update_event(text_1=text_1, text_2=text_2, text_3=text_3, page_id=table.id)

            except Exception as ex:
                log_error(ex)
                error_text = f'{error_text}\n❌ Не удалось обновить тексты {table.title}:\n{ex}'

            # проверить опции
            try:
                is_active = True if table.acell('B1').value == 'TRUE' else False
                title = table.acell ('B2').value
                event_date_str = table.acell ('B3').value
                event_time_str = table.acell ('B4').value
                event_datetime = datetime.strptime(
                    f'{event_date_str} {event_time_str}',
                    Config.datetime_form).replace(microsecond=0)

                await db.update_event (
                    is_active=is_active,
                    title=title,
                    new_date=event_datetime.date(),
                    new_time=event_datetime.time(),
                    page_id=table.id)

            except Exception as ex:
                log_error(ex)
                error_text = f'{error_text}\n❌ Не удалось обновить опции {table.title}:\n{ex}'

            # опции мест. Сначала удаляем все старые, записываем новые
            options = table.get_values ('A5:B9')

            old_event_options = await db.get_options(event_id=event.id)
            row_num = 5
            for option in options:
                try:
                    option_title = option[0]
                    empty_place = int(option[1])
                    cell = f'B{row_num}'
                    cell_f = table.acell (cell, value_render_option=ValueRenderOption.formula).value
                    all_place = int(cell_f.split('-')[0][1:])
                    option_id = None
                    # сохраняет id для тех кто заполняет заявку
                    if old_event_options:
                        old_option = [option for option in old_event_options if option.cell == cell]

                        if old_option:
                            option_id = old_option[0].id

                    row_num += 1

                    if option_id:
                        await db.update_option(
                            option_id=option_id,
                            title=option_title,
                            empty_place=empty_place,
                            all_place=all_place,
                            cell=cell
                        )
                    else:
                        await db.add_option(
                            event_id=event.id,
                            title=option_title,
                            empty_place=empty_place,
                            all_place=all_place,
                            cell=cell
                        )
                except Exception as ex:
                    log_error(ex)
                    error_text = f'{error_text}\n❌ Не удалось обновить места {table.title} {option[0]}:\n{ex}'

    return error_text


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
    page.update(range_name=cell, values=row)
