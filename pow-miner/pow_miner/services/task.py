import json
import subprocess
from pathlib import Path

import requests

from pow_miner.helpers import find_nonce, gpu_context
from pow_miner.infrastructure import RabbitMQClient
from pow_miner.schemas import Block, Task, TaskResult
from pow_miner.utils import Settings, logger


class TaskService:
    @property
    def is_gpu_available(self) -> bool:
        return gpu_context.get()

    @property
    def cuda_directory(self) -> Path:
        return Path.cwd() / "pow_miner/helpers/cuda/find_nonce.cu"

    @property
    def cuda_file(self) -> Path:
        return self.cuda_directory / "find_nonce.cu"

    @property
    def cuda_output_file(self) -> Path:
        return self.cuda_directory / "find_nonce_gpu"

    @property
    def cuda_result_file(self) -> Path:
        return self.cuda_directory / "output.json"

    def find_nonce_with_cpu(self, challenge: str, block: Block) -> TaskResult:
        logger.info("Computing nonce with CPU")
        result = find_nonce(
            target_hash_prefix=challenge,
            base_string=block.content,
            start_nonce=0,
            end_nonce=1000000,
        )
        return TaskResult(**result)

    def find_nonce_with_gpu(self, challenge: str, block: Block) -> TaskResult:
        logger.info("Computing nonce with GPU")

        if not self.cuda_output_file.is_file():
            logger.info("Compiling CUDA code...")
            subprocess.check_call(
                ["nvcc", str(self.cuda_file), "-o", str(self.cuda_output_file)]
            )

        subprocess.check_call(
            [str(self.cuda_output_file), "1", "10000", challenge, block.content],
            stdout=subprocess.DEVNULL,
        )

        with open(self.cuda_result_file, "r") as file:
            try:
                result = json.load(file)
                return TaskResult(**result)
            except json.JSONDecodeError:
                return TaskResult()

    async def mine(self, task: Task) -> None:
        try:
            challenge = task.challenge
            logger.info(f"Block: {task.data}")
            block = Block.model_validate(task.data)
            if self.is_gpu_available:
                result = self.find_nonce_with_gpu(challenge, block)
            else:
                result = self.find_nonce_with_cpu(challenge, block)
            logger.info(f"Mining result: {result}")
            if not result.hash_ or not result.nonce:
                return

            block = block.model_copy(
                update={
                    "hash_": result.hash_,
                    "nonce": result.nonce,
                }
            )
            logger.info(f"Sending block to orchestrator: {block}")
            requests.post(
                f"{Settings.BLOCK_ORCHESTRATOR_URL}/block/validate",
                block.model_dump_json(by_alias=True),
            )

        except Exception as e:
            logger.error(f"Error mining task: {e}")

    async def consume_tasks(self) -> Task | None:
        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        try:
            async with RabbitMQClient() as channel:
                queue_name = Settings.RABBITMQ_TASKS_QUEUE
                queue = await channel.declare_queue(queue_name, durable=True)
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            task = Task.model_validate_json(message.body)
                            await self.mine(task)
        except Exception as e:
            logger.error(f"Error consuming tasks: {e}")
            return None
