import asyncio
import logging
import sys
import logging

from handlers import dp
from config import DEBUG
from init import set_main_menu, bot, log_error
from db.base import init_models, db_command
from db.users import add_users
from db.events import add_events, get_events_t
from db.options import add_options


async def main() -> None:
    # await db_command()
    await init_models()
    await add_users()
    await add_events()
    # await get_events_t()
    # create_local_data_files()
    # await init_models()
    # logging.warning('ok')
    # await set_main_menu()
    # await bot.delete_webhook (drop_pending_updates=True)
    # await dp.start_polling(bot)
    pass


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start_bot', with_traceback=False)
    asyncio.run(main())
