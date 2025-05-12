import gspread
from gspread.exceptions import APIError
from gspread.utils import ValueRenderOption
from time import sleep
from datetime import datetime

import asyncio

import db
from init import bot
from settings import log_error, conf

import gspread_asyncio
from google.oauth2.service_account import Credentials


def get_creds():
    creds = Credentials.from_service_account_file(conf.google_key_path)
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)


# --- Обёртка для безопасного update ---
async def safe_update(worksheet, cell_range, values, raw: bool = True):
    max_retries = 10
    pause_sec = 2

    for attempt in range(max_retries):
        try:
            return await worksheet.update(cell_range, values, raw=raw)
        except APIError as e:
            if "Quota exceeded" in str(e):
                print(f"Превышена квота, попытка {attempt+1}/{max_retries}, жду {pause_sec} сек...")
                await asyncio.sleep(pause_sec)
            else:
                raise  # другие ошибки не глотаем
    raise Exception("Превышен лимит попыток записи в Google Sheets")


# --- Обёртка для безопасного update ---
async def safe_merge(worksheet, cell_range):
    max_retries = 10
    pause_sec = 2

    for attempt in range(max_retries):
        try:
            return await worksheet.merge_cells(cell_range)
        except APIError as e:
            if "Quota exceeded" in str(e):
                print(f"Превышена квота, попытка {attempt+1}/{max_retries}, жду {pause_sec} сек...")
                await asyncio.sleep(pause_sec)
            else:
                raise  # другие ошибки не глотаем
    raise Exception("Превышен лимит попыток записи в Google Sheets")


# добавляет данные в таблицу
async def create_new_page(date: str, time: str, title: str, tariffs: list[dict] = None, ticket_url: str = None) -> int:

    # gc = gspread.service_account(filename=Config.google_key_path)
    # table = agcm.open_by_key(Config.google_table_id)
    agc = await agcm.authorize()
    spreadsheet = await agc.open_by_key(conf.google_table_id)
    # table = await spreadsheet.worksheet(sheet_name)
    # проверка таблицы
    try:
        page = await spreadsheet.add_worksheet(title=title, cols=20, rows=200)
    except APIError as ex:
        log_error(ex)
        return 0

    # Настройки
    setting_list = [['Активна', ''],
                    ['Название', title],
                    ['Дата', date],
                    ['Время', time]]

    option_row = 5
    if tariffs:
        for tariff in tariffs:
            formula = f'={tariff["place"]}-SUMIFS(D:D; E:E; A{option_row})'
            setting_list.append([tariff["text"], formula])
            option_row += 1

    if ticket_url:
        setting_list.append(['Ссылка', ticket_url])

    # page.update(range_name=f'a1:b10', values=setting_list, raw=False)
    await safe_update(worksheet=page, cell_range=f'a1:b10', values=setting_list, raw=False)


    # page.merge_cells('E1:J3')
    # page.update(range_name='D1:1', values=[['Текст 1', info.text_1]])
    # sleep(1)
    # page.merge_cells('E4:J6')
    # page.update(range_name='D4:E4', values=[['Текст 2', info.text_2]])
    # sleep(1)
    # page.merge_cells('E7:J9')
    # page.update(range_name='D7:E7', values=[['Финальный текст', info.text_3]])
    # sleep(1)
    # тексты
    info = await db.Info.get_info()
    await safe_merge(worksheet=page, cell_range=f'E1:J3')
    await safe_update(worksheet=page, cell_range=f'D1:E1', values=[['Текст 1', info.text_1]])

    await safe_merge(worksheet=page, cell_range=f'E4:J6')
    await safe_update(worksheet=page, cell_range=f'D4:E4', values=[['Текст 2', info.text_2]])

    await safe_merge(worksheet=page, cell_range=f'E7:J9')
    await safe_update(worksheet=page, cell_range=f'D1:E1', values=[['Финальный текст', info.text_3]])

    # таблица гостей
    head_list = [['ID', 'Мест', 'Опции', 'Имя', 'Username', 'Телефон', 'Ссылка', 'Оплатил', 'Примечание', 'Откуда']]
    for i in range(0, 190):
        head_list.append(['', '', '-', '', '', '', '', '', '', ''])
    cells = f'c10:l200'
    # await page.update(range_name=cells, values=head_list)
    await safe_update(worksheet=page, cell_range=cells, values=head_list)

    # sleep(1)
    # триггер активности
    # page.update(range_name='C1', values=[['S']])

    return page.id


async def google_update(chat_id: int) -> str:
    error_text = ""

    sent = await bot.send_message(chat_id=chat_id, text='Загрузка данных')

    # авторизуемся и открываем таблицу
    agc = await agcm.authorize()
    spreadsheet = await agc.open_by_key(conf.google_table_id)

    await sent.edit_text('Обновление текстов')
    # обновляем базовые тексты
    try:
        sheet1 = await spreadsheet.get_worksheet(0)
        base_text_1 = (await sheet1.acell("E3")).value
        base_text_2 = (await sheet1.acell("E7")).value
        base_text_3 = (await sheet1.acell("E11")).value

        await db.Info.update_info(
            text_1=base_text_1,
            text_2=base_text_2,
            text_3=base_text_3,
        )
    except Exception as ex:
        log_error(ex)
        error_text += f"\n❌ Не удалось обновить базовые тексты: {ex}"

    # получаем список активных событий
    await sent.edit_text('Обновление мероприятий')

    active_events = await db.Event.get_events(active=True)
    active_page_ids = {e.page_id for e in active_events}

    # обходим все листы в таблице
    worksheets = await spreadsheet.worksheets()
    c = 0
    for ws in worksheets:
        if ws.id not in active_page_ids:
            continue

        event = await db.Event.get_event(page_id=ws.id)
        title = ws.title

        c += 1
        await sent.edit_text(f'Обновление мероприятий {c} {title}')

        # 1) обновляем тексты события
        try:
            text_1 = (await ws.acell("E1")).value
            text_2 = (await ws.acell("E4")).value
            text_3 = (await ws.acell("E7")).value

            await db.Event.update_event(
                page_id=ws.id,
                text_1=text_1,
                text_2=text_2,
                text_3=text_3,
            )
        except Exception as ex:
            log_error(ex)
            error_text += f"\n❌ Ошибка обновления текстов «{title}»: {ex}"

        # 2) обновляем настройки (дата, время, активность, заголовок)
        try:
            is_active = (await ws.acell("B1")).value.upper() == "TRUE"
            new_title = (await ws.acell("B2")).value
            date_str = (await ws.acell("B3")).value
            time_str = (await ws.acell("B4")).value
            dt = datetime.strptime(f"{date_str} {time_str}", conf.datetime_form)

            await db.Event.update_event(
                page_id=ws.id,
                is_active=is_active,
                title=new_title,
                new_date=dt.date(),
                new_time=dt.time(),
            )
        except Exception as ex:
            log_error(ex)
            error_text += f"\n❌ Ошибка обновления настроек «{title}»: {ex}"

        # 3) обновляем варианты мест
        try:
            options = await ws.get_values("A5:B9")
            old_opts = await db.Option.get_options(event_id=event.id)
            row_num = 5

            for opt in options:
                option_name, empty_str = opt
                empty_place = int(empty_str)
                cell_ref = f"B{row_num}"

                formula_cell = await ws.acell(cell_ref, value_render_option=ValueRenderOption.formula)
                all_place = int(formula_cell.value.split("-")[0].lstrip("="))

                # ищем существующую опцию по cell
                matching = [o for o in old_opts if o.cell == cell_ref]
                if matching:
                    await db.Option.update_option(
                        option_id=matching[0].id,
                        name=option_name,
                        empty_place=empty_place,
                        all_place=all_place,
                        cell=cell_ref,
                    )
                else:
                    await db.Option.add_option(
                        event_id=event.id,
                        name=option_name,
                        empty_place=empty_place,
                        all_place=all_place,
                        cell=cell_ref,
                    )
                row_num += 1

        except Exception as ex:
            log_error(ex)
            error_text += f"\n❌ Ошибка обновления мест «{title}»: {ex}"

    await sent.delete()
    return error_text


async def add_new_order_in_table(
    count_place: int,
    option: str,
    name: str,
    phone: str,
    page_id: int,
    order_id: int,
    username: str,
) -> None:
    """
    Асинхронно добавляет новую заявку в Google Sheet,
    используя safe_update для записи с повторными попытками.
    """
    try:
        agc = await agcm.authorize()
        spreadsheet = await agc.open_by_key(conf.google_table_id)
        worksheets = await spreadsheet.worksheets()
        # ищем лист по его internal id
        page = next((ws for ws in worksheets if ws.id == page_id), None)
        if page is None:
            raise ValueError(f"Worksheet with id {page_id} not found")

        # считываем существующие строки C11:C200
        client_table = await page.get_values("C11:C200")
        empty_row = len(client_table) + 11
        for idx, row in enumerate(client_table):
            if row == ["-"] or row == []:
                empty_row = idx + 11
                break

        # готовим данные для записи
        if not username:
            username_display = ""
            link = f"https://t.me/+{phone}"
        else:
            username_display = f"@{username}"
            link = f"https://t.me/{username}"

        row_values = [[order_id, count_place, option, name, username_display, phone, link]]
        cell_range = f"C{empty_row}:I{empty_row}"

        # небольшая пауза перед записью
        await asyncio.sleep(1)
        await safe_update(page, cell_range, row_values)

    except Exception as ex:
        log_error(f"add_new_order_in_table failed: {ex}")
        raise



# async def google_update() -> str:
#     error_text = ''
#     gc = gspread.service_account (filename=Config.google_key_path)
#     tables = gc.open_by_key (Config.google_table_id)
#
#     agc = await agcm.authorize()
#     tables = await agc.open_by_key(conf.google_table_id)
#     tables.get_sheet1()
#     # обновляем настройки
#     try:
#         sheet1 = await tables.get_sheet1()
#         base_text_1 = await sheet1.acell('E3').value
#         base_text_2 = tables.get_sheet1.acell('E7').value
#         base_text_3 = tables.get_sheet1.acell('E11').value
#
#         await db.Info.update_info(text_1=base_text_1, text_2=base_text_2, text_3=base_text_3)
#     except Exception as ex:
#         log_error(ex)
#         error_text = f'{error_text}\n❌ Не удалось обновить базовые тексты:\n{ex}'
#
#     active_events = await db.get_events(active=True)
#     active_page_ids = [event.page_id for event in active_events]
#     for table in tables:
#         if table.id in active_page_ids:
#             event = await db.get_event(page_id=table.id)
#             # проверить тексты
#             try:
#                 text_1 = table.acell('E1').value
#                 text_2 = table.acell('E4').value
#                 text_3 = table.acell('E7').value
#
#                 await db.update_event(text_1=text_1, text_2=text_2, text_3=text_3, page_id=table.id)
#
#             except Exception as ex:
#                 log_error(ex)
#                 error_text = f'{error_text}\n❌ Не удалось обновить тексты {table.title}:\n{ex}'
#
#             # проверить опции
#             try:
#                 is_active = True if table.acell('B1').value == 'TRUE' else False
#                 title = table.acell ('B2').value
#                 event_date_str = table.acell ('B3').value
#                 event_time_str = table.acell ('B4').value
#                 event_datetime = datetime.strptime(
#                     f'{event_date_str} {event_time_str}',
#                     Config.datetime_form).replace(microsecond=0)
#
#                 await db.update_event (
#                     is_active=is_active,
#                     title=title,
#                     new_date=event_datetime.date(),
#                     new_time=event_datetime.time(),
#                     page_id=table.id)
#
#             except Exception as ex:
#                 log_error(ex)
#                 error_text = f'{error_text}\n❌ Не удалось обновить опции {table.title}:\n{ex}'
#
#             # опции мест. Сначала удаляем все старые, записываем новые
#             options = table.get_values ('A5:B9')
#
#             old_event_options = await db.get_options(event_id=event.id)
#             row_num = 5
#             for option in options:
#                 try:
#                     option_title = option[0]
#                     empty_place = int(option[1])
#                     cell = f'B{row_num}'
#                     cell_f = table.acell (cell, value_render_option=ValueRenderOption.formula).value
#                     all_place = int(cell_f.split('-')[0][1:])
#                     option_id = None
#                     # сохраняет id для тех кто заполняет заявку
#                     if old_event_options:
#                         old_option = [option for option in old_event_options if option.cell == cell]
#
#                         if old_option:
#                             option_id = old_option[0].id
#
#                     row_num += 1
#
#                     if option_id:
#                         await db.update_option(
#                             option_id=option_id,
#                             title=option_title,
#                             empty_place=empty_place,
#                             all_place=all_place,
#                             cell=cell
#                         )
#                     else:
#                         await db.add_option(
#                             event_id=event.id,
#                             title=option_title,
#                             empty_place=empty_place,
#                             all_place=all_place,
#                             cell=cell
#                         )
#                 except Exception as ex:
#                     log_error(ex)
#                     error_text = f'{error_text}\n❌ Не удалось обновить места {table.title} {option[0]}:\n{ex}'
#
#     return error_text


# проверка обновлений
# def add_new_order_in_table(
#         count_place: int,
#         option: str,
#         name: str,
#         phone: str,
#         page_id: int,
#         order_id: int,
#         username: str
# ) -> None:
#     gc = gspread.service_account(filename=Config.google_key_path)
#     table = gc.open_by_key(Config.google_table_id)
#     page = table.get_worksheet_by_id(page_id)
#     client_table = page.get(f'C11:C200')
#
#     empty_row_index = len(client_table) + 11
#     for i, row in enumerate(client_table):
#         if row == ['-'] or row == []:
#             empty_row_index = i + 11  # Прибавляем 10, чтобы получить номер строки в таблице
#             break
#
#     if not username:
#         username = ''
#         link = f'https://t.me/+{phone}'
#     else:
#         link = f'https://t.me/{username}'
#         username = f'@{username}'
#
#     row = [[order_id, count_place, option, name, username, phone, link]]
#     cell = f'C{empty_row_index}:I{empty_row_index}'
#     sleep(1)
#     page.update(range_name=cell, values=row)
