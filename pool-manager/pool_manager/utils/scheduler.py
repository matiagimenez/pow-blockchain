from typing import Awaitable, Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pool_manager.utils.logger import logger


class Scheduler_:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self) -> None:
        logger.info("Starting scheduler...")
        self.scheduler.start()

    def add_cronjob(self, job: Callable[[], Awaitable[None]], interval: int) -> None:
        logger.info(f"Adding cronjob to scheduler - {job.__name__}")
        self.scheduler.add_job(job, "interval", seconds=interval)


Scheduler = Scheduler_()
