from typing import Optional, Tuple, Union

import aioredis
from aioredis import Redis
from loguru import logger
from src.settings import settings


class RedisClient:
    """
    Super simple redis client.
    """
    def __init__(self, address: Union[str, Tuple[str, int]], password: str):
        self.address = address
        self.password = password
        self._client: Optional[Redis] = None

    async def create_pool(self) -> None:
        logger.debug("Creating redis pool")
        self._client = await aioredis.create_redis_pool(
            self.address, password=self.password
        )
        logger.debug("Redis pool created")

    @property
    def client(self) -> Redis:
        """
        Get actual Redis client.
        :return:
        """
        if self._client is None:
            raise Exception("Not connected to redis")
        return self._client

    async def shutdown(self) -> None:
        """
        Shutdown session for redis.
        Close redis pool.
        """
        logger.debug("Shutting down redis")
        if self._client is None:
            return
        self._client.close()
        await self._client.wait_closed()
        logger.debug("Redis connection pool closed")


redis = RedisClient(
    address=(settings.redis_host, settings.redis_port), password=settings.redis_password
)
