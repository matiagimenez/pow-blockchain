from aio_pika import Message
from block_orchestrator.infrastructure import RabbitMQClient, RedisClient
from block_orchestrator.schemas import Transaction
from block_orchestrator.utils import Settings, logger


class TransactionService:
    async def publish_transaction(self, transaction: Transaction) -> None:
        try:
            await self._store_transaction(transaction)
            await self._publish_to_queue(transaction)

            logger.info(f"Successfully processed transaction {transaction.id_}")
        except Exception as e:
            logger.error(
                f"Failed to publish transaction {transaction.id_}: {e}", exc_info=True
            )
            raise

    async def _store_transaction(self, transaction: Transaction) -> None:
        async with RedisClient() as redis:
            await redis.hset(
                str(transaction.id_),
                mapping=transaction.model_dump(by_alias=True, mode="json"),
            )
        logger.info(f"Stored transaction {transaction.id_} in database")

    async def _publish_to_queue(self, transaction: Transaction) -> None:
        async with RabbitMQClient() as channel:
            exchange = await channel.get_exchange(Settings.RABBITMQ_EXCHANGE)
            await exchange.publish(
                Message(
                    body=transaction.model_dump_json(by_alias=True).encode("utf-8")
                ),
                routing_key=Settings.RABBITMQ_QUEUES["transactions"],
            )

        logger.info(f"Published transaction {transaction.id_} to queue")
