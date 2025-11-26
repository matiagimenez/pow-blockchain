from fastapi import APIRouter, HTTPException, status

from block_orchestrator.schemas import Block

from .dependencies import InjectedBlockService

blocks_router = APIRouter(tags=["Blocks"], prefix="/blocks")


@blocks_router.get("/")
async def get_blocks(service: InjectedBlockService) -> list[Block]:
    return await service.get_blocks()


@blocks_router.post("/validate")
async def submit_block(block: Block, service: InjectedBlockService) -> Block:
    if not block.is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Block {block.hash_} validation failed",
        )

    block_already_exists = await service.verify_block_existance(block)
    if block_already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Block already exists in the blockchain",
        )

    await service.add_block_to_chain(block)
    return block
