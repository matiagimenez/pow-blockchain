from __future__ import annotations

import asyncio
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractChannel

from src.utils import Settings


class RabbitMQClient:
    def __init__(self):
        self.max_retries = Settings.RABBITMQ_MAX_RETRIES
        self.retry_delay = Settings.RABBITMQ_RETRY_DELAY
        self._connection = None
        self._channel = None

    async def __aenter__(self) -> AbstractChannel:
        await self.connect()
        return self._channel

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def connect(self) -> AbstractChannel:
        for attempt in range(1, self.max_retries + 1):
            try:
                self._connection = await connect_robust(
                    host=Settings.RABBITMQ_HOST,
                    login=Settings.RABBITMQ_USER,
                    password=Settings.RABBITMQ_PASSWORD,
                    heartbeat=3600,
                )

                self._channel = await self._connection.channel()
                await self._setup_exchanges_and_queues()
                return self._channel

            except Exception:
                if attempt == self.max_retries:
                    raise
                await asyncio.sleep(self.retry_delay)

        raise RuntimeError("Failed to connect to RabbitMQ after retries")

    async def close(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()

    async def _setup_exchanges_and_queues(self):
        if not self._channel:
            raise RuntimeError("Channel not initialized")

        exchange = await self._channel.declare_exchange(
            name=Settings.RABBITMQ_EXCHANGE,
            type=ExchangeType.DIRECT,
            durable=True,
            auto_delete=False,
        )

        for name, routing_key in Settings.RABBITMQ_QUEUES.items():
            queue = await self._channel.declare_queue(name=name, durable=True)
            await queue.bind(exchange, routing_key)
