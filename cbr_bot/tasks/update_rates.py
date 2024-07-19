import asyncio
import logging
from datetime import date
from typing import Optional

from redis.asyncio.client import Pipeline

from cbr_bot.api import get_rates, get_current_date
from cbr_bot.database import redis


async def update_rates(period: int = 3600):
    is_first: bool = True

    while True:
        try:
            if not is_first:
                await asyncio.sleep(period)

            is_first = False
            current_date: Optional[date] = await get_current_date()
            last_update: Optional[bytes] = await redis.get("last_update")

            if last_update is not None and current_date == date.fromisoformat(last_update.decode("utf-8")):
                continue

            rates: Optional[dict] = await get_rates()

            if rates is None:
                continue

            pipeline: Pipeline = redis.pipeline()
            await pipeline.set("last_update", str(current_date))

            for code, rate in rates.items():
                await pipeline.set(f"currency:{code}", rate)

            await pipeline.execute()
        except Exception as _ex:
            logging.warning(_ex)
