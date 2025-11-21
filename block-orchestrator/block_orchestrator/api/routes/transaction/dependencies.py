from typing import Annotated

from block_orchestrator.services import TransactionService
from fastapi import Depends

InjectedTransactionService = Annotated[TransactionService, Depends(TransactionService)]
