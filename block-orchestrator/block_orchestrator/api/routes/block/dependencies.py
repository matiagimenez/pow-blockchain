from typing import Annotated

from block_orchestrator.services import BlockService
from fastapi import Depends

InjectedBlockService = Annotated[BlockService, Depends(BlockService)]
