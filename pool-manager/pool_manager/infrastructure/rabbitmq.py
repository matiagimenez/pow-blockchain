from __future__ import annotations

import asyncio

from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import AbstractChannel

from pool_manager.utils import Settings, logger


class RabbitMQClient:
    def __init__(self) -> None:
        self.max_retries = Settings.CONNECTION_MAX_RETRIES
        self.retry_delay = Settings.CONNECTION_RETRY_DELAY
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
                logger.info("Attempting to connect to RabbitMQ...")
                self._connection = await connect_robust(
                    host=Settings.RABBITMQ_HOST,
                    port=Settings.RABBITMQ_PORT,
                    login=Settings.RABBITMQ_USER,
                    password=Settings.RABBITMQ_PASSWORD,
                    heartbeat=3600,
                )
                self._channel = await self._connection.channel()  # type: ignore[attr-defined]
                await self._setup_exchanges_and_queues()

                logger.info("Connected to RabbitMQ successfully")
                return self._channel

            except Exception:
                if attempt == self.max_retries:
                    raise
                logger.warning(
                    f"Failed to connect to RabbitMQ. Retrying in {self.retry_delay} seconds..."
                )
                await asyncio.sleep(self.retry_delay)

        raise RuntimeError("Failed to connect to RabbitMQ after retries")

    async def close(self):
        if self._channel and not self._channel.is_closed:
            logger.info("Closing RabbitMQ channel")
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            logger.info("Closing RabbitMQ connection")
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

        queues = {
            Settings.RABBITMQ_TRANSACTIONS_QUEUE: Settings.RABBITMQ_TRANSACTIONS_ROUTING_KEY,
            Settings.RABBITMQ_TASKS_QUEUE: Settings.RABBITMQ_TASKS_ROUTING_KEY,
        }

        for queue_name, routing_key in queues.items():
            queue = await self._channel.declare_queue(name=queue_name, durable=True)
            await queue.bind(exchange, routing_key)
