import os

from redis.asyncio import Redis

host: str = os.getenv("REDIS_HOST")

redis: Redis = Redis(host=host)
