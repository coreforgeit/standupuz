from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from db import Event
from init import scheduler, redis_client_1
from settings import log_error
from enums import Key


# запускает планировщики
async def start_schedulers():
    scheduler.add_job(
        func=Event.close_old_events,
        trigger=CronTrigger(hour=1),
        id=Key.CLOSE_EVENT.value,
        replace_existing=True,
    )
    scheduler.add_job(
        func=print_scheduled_jobs,
        trigger=IntervalTrigger(hours=1),
        id='print_scheduled_jobs',
        replace_existing=True,
    )
    scheduler.start()
    print_scheduled_jobs()


# тормозит планировщики
async def shutdown_schedulers():
    scheduler.remove_job(job_id=Key.CLOSE_EVENT.value)
    scheduler.remove_job(job_id='print_scheduled_jobs')
    scheduler.shutdown()


# показывает все запланированные работ
def print_scheduled_jobs():
    jobs = scheduler.get_jobs()
    s_log = [f"\nЗапланировано {len(jobs)} задач(и):"]

    for job in jobs:
        # Попробуем получить TTL по ключу Redis
        redis_key = f'apscheduler.jobs'  # основной ключ, где хранятся job'ы
        # ttl = await redis.ttl(redis_key)
        ttl = redis_client_1.ttl(redis_key)

        s_log.append(f"- ID: {job.id}")
        s_log.append(f"  Функция: {job.func_ref}")
        s_log.append(f"  Триггер: {job.trigger}")
        s_log.append(f"  Следующий запуск: {job.next_run_time}")
        s_log.append(f"  TTL ключа jobs: {ttl if ttl >= 0 else '∞'} секунд")
        s_log.append("—" * 10)

    log_error('\n'.join(s_log), wt=False)
