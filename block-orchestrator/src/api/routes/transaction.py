from aio_pika import Message
from fastapi import APIRouter, status
from src.infrastructure import RabbitMQClient
from src.schemas import Transaction
from src.utils import Settings, logger

transaction_router = APIRouter(tags=["Transactions"], prefix="/transaction")

@transaction_router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def register_transaction(transaction: Transaction) -> Transaction:
    async with RabbitMQClient() as channel:
        try:
            logger.info(f"Registering transaction {transaction.model_dump_json(indent=4)}")
            exchange = await channel.get_exchange(Settings.RABBITMQ_EXCHANGE)
            await exchange.publish(
                routing_key='tx',
                message=Message(body=transaction.model_dump_json(by_alias=True).encode('utf-8'))
            )
            logger.info(f"Published transaction {transaction.id_} to queue")
        # Almacenar la transacción en redis.
        # redis.hset(transaction_id, mapping=transaction.model_dump(by_alias=True))
            return transaction
        except Exception:
            raise ValueError("Failed to register transaction")