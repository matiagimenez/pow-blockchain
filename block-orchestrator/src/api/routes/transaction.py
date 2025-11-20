from aio_pika import Message
from fastapi import APIRouter
from src.schemas import Transaction
from src.infrastructure import RabbitMQClient
from fastapi import status
from src.utils import Settings

transaction_router = APIRouter(tags=["Transactions"], prefix="/transaction")

@transaction_router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def register_transaction(transaction: Transaction) -> Transaction:
    async with RabbitMQClient() as channel:
        try:
            exchange = await channel.get_exchange(Settings.RABBITMQ_EXCHANGE)
            await exchange.publish(
                routing_key='tx',
                message=Message(body=transaction.model_dump_json(by_alias=True).encode('utf-8'))
            )
        # Almacenar la transacción en redis.
        # redis.hset(transaction_id, mapping=transaction.model_dump(by_alias=True))
            return transaction
        except Exception as e:
            raise ValueError("Failed to register transaction")