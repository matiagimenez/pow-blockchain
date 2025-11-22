from block_orchestrator.services import BlockService, TransactionService
from block_orchestrator.utils import logger


async def process_transactions_and_build_block() -> None:
    """
    Scheduled task that processes pending transactions and builds a new block.
    """
    try:
        logger.info("Starting scheduled task: process transactions and build block")

        transaction_service = TransactionService()
        block_service = BlockService()

        transactions = await transaction_service.process_transactions()

        if not transactions:
            logger.info("No transactions to process")
            return

        logger.info(f"Processed {len(transactions)} transactions")

        await block_service.build_block(transactions)
    except Exception as e:
        logger.error(f"Error in scheduled task: {e}", exc_info=True)
