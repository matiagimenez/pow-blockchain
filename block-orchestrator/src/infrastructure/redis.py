import asyncio
import os
from typing import Optional

from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from src.utils import Settings

class RedisClient:
    def __init__(self):
        self.host = Settings.REDIS_HOST
        self.port = Settings.REDIS_PORT
        self.password = Settings.REDIS_PASSWORD
        self.max_retries = Settings.CONNECTION_MAX_RETRIES
        self.retry_delay = Settings.CONNECTION_RETRY_DELAY

        self._client: Optional[Redis] = None

    async def __aenter__(self) -> Redis:
        await self.connect()
        return self._client

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def connect(self) -> Redis:
        for attempt in range(1, self.max_retries + 1):
            try:
                self._client = Redis(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    decode_responses=True,
                )

                self._client.ping()
                return self._client

            except ConnectionError:
                if attempt == self.max_retries:
                    raise
                print(f"Failed to connect to Redis. Retrying in {self.retry_delay} seconds...")
                await asyncio.sleep(self.retry_delay)
        raise RuntimeError("Redis connection failed after retries.")

    async def close(self):
        if self._client:
            await self._client.close()
