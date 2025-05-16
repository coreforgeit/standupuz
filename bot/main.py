import asyncio
import sys
import logging

from aiogram import Dispatcher

import db
from handlers import client_router
from handlers.main_menu import main_router
from handlers.exceptions import error_router
from settings import conf, log_error
from init import set_main_menu, bot
from db.base import init_models
from utils import start_schedulers, shutdown_schedulers


dp = Dispatcher()


async def main() -> None:
    await init_models()
    await set_main_menu()
    if not conf.debug:
        await start_schedulers()
        await db.Event.close_old_events()
    else:
        pass
        await start_schedulers()
    dp.include_router(main_router)
    dp.include_router(client_router)
    dp.include_router(error_router)
    await dp.start_polling(bot)
    if not conf.debug:
        await shutdown_schedulers()
    await bot.session.close()


if __name__ == "__main__":
    if conf.debug:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start_bot', wt=False)
    asyncio.run(main())
