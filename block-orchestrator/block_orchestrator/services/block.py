from datetime import datetime

from aio_pika import Message

from block_orchestrator.infrastructure import RabbitMQClient, RedisClient
from block_orchestrator.schemas import Block, Task, Transaction
from block_orchestrator.utils import Settings, logger


class BlockService:
    async def verify_block_existance(self, block: Block) -> bool:
        try:
            logger.info(
                f"Verifying existence of block {block.model_dump(by_alias=True)}"
            )
            async with RedisClient() as redis:
                previous_block_key = f"b-{block.previous_hash}"
                return await redis.hexists(previous_block_key, "hash")
        except Exception as e:
            logger.error(f"Failed to verify block {block.hash_} existance: {e}")
            raise

    async def build_block(self, transactions: list[Transaction]) -> None:
        logger.info("Building new block...")

        async with RedisClient() as redis:
            last_block_hash = await redis.zrange("hashes", -1, -1, withscores=True)

            if not last_block_hash:
                # Genesis block
                previous_hash = "0"
                last_index = 0
            else:
                last_index = await redis.zcount("hashes", "-inf", "+inf")
                previous_hash = last_block_hash[0][0]

        block = Block(
            index=last_index,
            transactions=transactions,
            previous_hash=previous_hash,
        )
        task = Task(data=block.to_dict())

        async with RabbitMQClient() as channel:
            exchange = await channel.get_exchange(Settings.RABBITMQ_EXCHANGE)
            await exchange.publish(
                Message(
                    body=task.model_dump_json().encode("utf-8"),
                    delivery_mode=2,
                ),
                routing_key=Settings.RABBITMQ_TASKS_ROUTING_KEY,
            )

        logger.info(
            f"Block {block.index} created and sent to miners - "
            f"previous_hash={block.previous_hash}"
        )

    async def add_block_to_chain(self, block: Block) -> None:
        try:
            logger.info(f"Adding block to chain {block.model_dump(by_alias=True)}")

            block_key = f"b-{block.previous_hash}"
            timestamp = int(datetime.now().timestamp())
            async with RedisClient() as redis:
                await redis.zadd("hashes", {block.hash_: timestamp})
                await redis.hset(block_key, mapping=block.to_dict())
        except Exception as e:
            logger.error(f"Failed to add block to chain {block.hash_}: {e}")
            raise
