from block_orchestrator.schemas import Transaction
from block_orchestrator.utils import logger
from fastapi import APIRouter, BackgroundTasks, status

from .dependencies import InjectedTransactionService

transactions_router = APIRouter(tags=["Transactions"], prefix="/transaction")


@transactions_router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def register_transaction(
    transaction: Transaction,
    background_tasks: BackgroundTasks,
    service: InjectedTransactionService
) -> Transaction:
    logger.info(f"Registering transaction {transaction.model_dump_json(indent=4)}")
    background_tasks.add_task(service.publish_transaction, transaction)
    return transaction