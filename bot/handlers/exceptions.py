from aiogram.types import ErrorEvent

import db
from init import dp, bot, log_error


@dp.errors()
async def errors_handler(ex: ErrorEvent):
    log_error(ex)
