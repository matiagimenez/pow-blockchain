from datetime import datetime

from block_orchestrator.infrastructure import RedisClient
from block_orchestrator.schemas import Block
from block_orchestrator.utils import logger


class BlockService:
    async def verify_block_existance(self, block: Block) -> bool:
        try:
            logger.info(
                f"Verifying existence of block "
                f"{block.model_dump_json(indent=4, exclude={'transactions'})}"
            )
            async with RedisClient() as redis:
                previous_block_id = f"blockchain:{block.previous_hash}"
                return await redis.hexists(previous_block_id, "hash")
        except Exception as e:
            logger.error(f"Failed to verify block {block.hash_} existance: {e}")
            raise

    async def add_block_to_chain(self, block: Block) -> None:
        try:
            logger.info(
                f"Adding block to chain "
                f"{block.model_dump_json(indent=4, exclude={'transactions'})}"
            )
            block_key = f"blockchain:{block.previous_hash}"
            timestamp = datetime.now().timestamp()
            async with RedisClient() as redis:
                await redis.zadd("block_hashes", {block.hash_: timestamp})
                await redis.hset(
                    block_key, mapping=block.model_dump(by_alias=True, mode="json")
                )
        except Exception as e:
            logger.error(f"Failed to add block to chain {block.hash_}: {e}")
            raise
