from block_orchestrator.services import TransactionService
from block_orchestrator.infrastructure import RabbitMQClient, RedisClient
from typing import Annotated
from fastapi import Depends

def inject_transaction_service() -> TransactionService:
    return TransactionService(
        db_client=RedisClient(),
        queue_client=RabbitMQClient(),
    )

InjectedTransactionService = Annotated[TransactionService, Depends(inject_transaction_service)]