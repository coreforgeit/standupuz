import asyncio

import db
import keyboards as kb
from init import bot
from settings import log_error, conf
from utils.google_utils import add_new_order_in_table
from utils.entities_utils import recover_entities


async def send_event(event_id: int, user_id: int, from_start: bool = False) -> None:
    event_info = await db.Event.get_event(event_id)
    entities = recover_entities(event_info.entities)
    options = await db.Option.get_options(event_id)

    photo_id = event_info.photo_id
    # if DEBUG:
    #     photo_id = 'AgACAgIAAxkBAAMGZecrNFZ3ctI1jBQlYNCIneaND5IAAkTaMRuSRDhLC7cywGea_iYBAAMCAAN5AAM0BA'
    await bot.send_photo(
        chat_id=user_id,
        photo=photo_id,
        caption=event_info.text,
        caption_entities=entities,
        parse_mode=None,
        reply_markup=kb.get_book_kb(options=options, ticket_url=event_info.ticket_url, from_start=from_start)
    )


# добавляет пользователя в таблицу
async def end_book(data: dict):
    # запись в таблицу, запись в базу, оповещение
    await db.Option.update_option(option_id=data['option_id'], edit_place=0 - data['count_place'])
    option_info = await db.Option.get_option(option_id=data['option_id'])
    order_id = await db.Order.add_order(
        user_id=data['user_id'],
        phone=data['phone'],
        event_id=data['event_id'],
        option=option_info.name,
        count_place=data['count_place'],
        page_id=data['page_id'])

    i = 0
    try:
        await add_new_order_in_table(
            count_place=data['count_place'],
            option=option_info.name,
            name=data['name'],
            phone=data['phone'],
            page_id=data['page_id'],
            order_id=order_id,
            username=data['username']
        )
        in_table = True
        await db.Order.update_order(order_id=order_id, in_google=True)
        text = f'Новая бронь:\n' \
               f'{option_info.name} - {data["count_place"]}\n' \
               f'{data["event_title"]}\n' \
               f'{data["name"]}\n' \
               f'{data["phone"]}\n'

        await bot.send_message(conf.admin_group_id, text)

    except Exception as ex:
        i += 1
        if i > 30:
            in_table = 'error'
            log_error(f'end try add row {i} {ex}', wt=False)
            text = (f'‼️ ОШИБКА! Ваша бронь не была добавлена. Попробуйте ещё раз. Если ошибка будет повторяться, '
                    f'обратитесь в поддержку')
            await bot.send_message(data['user_id'], text)
        else:
            log_error(f'try add row {i} {ex}', wt=False)
            await asyncio.sleep(5)
