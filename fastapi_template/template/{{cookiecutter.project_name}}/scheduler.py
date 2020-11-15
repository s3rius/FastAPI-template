import asyncio

import aioschedule as schedule
from loguru import logger

from src.settings import settings


async def scheduled_task() -> None:
    logger.info("I was scheduled to run now")


schedule.every(settings.schedule_timer).seconds.do(scheduled_task)

if __name__ == "__main__":
    logger.debug("Started scheduler")
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(schedule.run_pending())