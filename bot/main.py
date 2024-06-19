import asyncio
import logging
import sys

from handlers import dp
from config import DEBUG
from init import set_main_menu, bot, log_error
from db.base import init_models
# from db.users import add_users
from db.events import add_events


async def main() -> None:
    # await init_models()
    # await add_events()
    # create_local_data_files()
    await init_models()
    await set_main_menu()
    # if not DEBUG:
    #     await start_scheduler()
    await bot.delete_webhook (drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start_bot', with_traceback=False)
    asyncio.run(main())
