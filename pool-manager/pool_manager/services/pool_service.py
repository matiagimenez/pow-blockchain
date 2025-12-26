import json
import time
from typing import Any

from aio_pika import DeliveryMode, IncomingMessage, Message

from pool_manager.infrastructure import GoogleCloudClient, RabbitMQClient, RedisClient
from pool_manager.schemas import Block, MiningTask
from pool_manager.utils import Settings, logger


class PoolService:
    def __init__(self):
        self.rabbitmq = RabbitMQClient()
        self.gcp = GoogleCloudClient()

    async def start(self) -> None:
        await self.rabbitmq.connect()
        queue_name = Settings.RABBITMQ_TASKS_QUEUE
        queue = await self.rabbitmq._channel.get_queue(queue_name)
        await queue.consume(self.process_task)
        logger.info("Started consuming tasks")

    async def stop(self) -> None:
        await self.rabbitmq.close()

    async def process_task(self, message: IncomingMessage) -> None:
        async with message.process():
            try:
                body = message.body.decode()
                mining_task = MiningTask.model_validate_json(body)

                logger.info(f"Processing task with challenge: {mining_task.challenge}")
                block = Block.model_validate(mining_task.data)

                await self.create_mining_subtasks(block, mining_task.challenge)
            except Exception as e:
                logger.error(f"Error processing task: {e}")

    async def create_mining_subtasks(self, block: Block, challenge: str) -> bool:
        try:
            gpu_miners_alive = await self.get_gpu_active_nodes()

            miners_count, challenge = self._get_mining_config(gpu_miners_alive)
            range_interval = self._calculate_range_interval(miners_count)

            range_from = 1
            range_to = range_interval

            logger.info(f"Creating subtasks for {miners_count} miners")

            for _ in range(miners_count):
                subtask = {
                    "start_nonce": range_from,
                    "end_nonce": range_to,
                    "challenge": challenge,
                    "data": block.to_dict(),
                }

                range_from = range_to + 1
                range_to += range_interval

                await self.publish_subtask(subtask)
            return True
        except Exception as e:
            logger.error(f"Error creating mining subtasks: {e}")
            return False

    async def publish_subtask(self, subtask: dict[str, Any]) -> None:
        exchange = await self.rabbitmq._channel.get_exchange(Settings.RABBITMQ_EXCHANGE)
        await exchange.publish(
            Message(
                body=json.dumps(subtask).encode(), delivery_mode=DeliveryMode.PERSISTENT
            ),
            routing_key=Settings.RABBITMQ_SUBTASKS_ROUTING_KEY,
        )

    async def get_worker_keys(self, pattern: str = "worker-*") -> list[str]:
        async with RedisClient() as redis:
            cursor = "0"
            worker_keys = []
            while cursor != 0:
                cursor, keys = await redis.scan(cursor=cursor, match=pattern)
                worker_keys.extend(keys)
            return worker_keys

    async def check_node_status(self, node_id: str) -> bool:
        try:
            current_time = int(time.time())
            async with RedisClient() as redis:
                last_keep_alive = await redis.hget(node_id, "last_keep_alive")

                if last_keep_alive:
                    last_keep_alive = int(last_keep_alive)
                    if current_time - last_keep_alive <= Settings.EXPIRATION_TIME:
                        return True

                    logger.info(f"Node {node_id} expired")
                    await redis.delete(node_id)
                    return False
                return False
        except Exception as e:
            logger.error(f"Error checking node status: {e}")
            return False

    async def get_gpu_active_nodes(self) -> int:
        try:
            gpu_active_nodes = 0
            all_nodes = await self.get_worker_keys()
            for node_id in all_nodes:
                if await self.check_node_status(node_id):
                    gpu_active_nodes += 1
            return gpu_active_nodes
        except Exception as e:
            logger.error(f"Error getting GPU active nodes: {e}")
            return 0

    async def check_pool_status(self) -> None:
        try:
            gpu_active_nodes = await self.get_gpu_active_nodes()
            logger.info(f"Active GPU workers: {gpu_active_nodes}")

            if gpu_active_nodes > 0:
                logger.info("GPU miners active")
                if self.gcp.get_active_instance_count() > 0:
                    self.gcp.destroy_all_instances()
            else:
                logger.info("No GPU miners active")
                if self.gcp.get_active_instance_count() == 0:
                    logger.info(f"Creating {Settings.CPU_MINERS_COUNT} CPU instances")
                    self.gcp.create_multiple_instances(Settings.CPU_MINERS_COUNT)

        except Exception as e:
            logger.error(f"Error checking pool status: {e}")

    def _get_mining_config(self, gpu_miners_alive: int) -> tuple[int, str]:
        if gpu_miners_alive > 0:
            logger.info(
                f"GPU miners active, using challenge: {Settings.GPU_HASH_CHALLENGE}"
            )
            return gpu_miners_alive, Settings.GPU_HASH_CHALLENGE

        logger.info(
            f"CPU miners active, using challenge: {Settings.CPU_HASH_CHALLENGE}"
        )
        return self.gcp.get_active_instance_count(), Settings.CPU_HASH_CHALLENGE

    def _calculate_range_interval(self, miners_count: int) -> int:
        if miners_count == 0:
            return Settings.MAX_RANGE
        return round(Settings.MAX_RANGE / miners_count)
