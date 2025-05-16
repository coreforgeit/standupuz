from apscheduler.triggers.cron import CronTrigger

from db import Event
from init import scheduler
from enums import Key


# запускает планировщики
async def start_schedulers():
    scheduler.add_job(
        func=Event.close_old_events,
        trigger=CronTrigger(hour=6),
        id=Key.CLOSE_EVENT.value,
        replace_existing=True,
    )
    scheduler.start()


# тормозит планировщики
async def shutdown_schedulers():
    scheduler.remove_job(job_id=Key.CLOSE_EVENT.value)
    scheduler.shutdown()
