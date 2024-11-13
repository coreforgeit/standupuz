from aiogram.types import ErrorEvent

from init import dp, log_error


@dp.errors()
async def errors_handler(ex: ErrorEvent):
    log_error(ex)
