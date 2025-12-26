import random
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from pool_manager.infrastructure import RedisClient

from .schemas import NodeKeepAliveRequest

router = APIRouter(prefix="/nodes", tags=["Nodes"])


# TODO:  Update the keep alive signal request in pow-miner - replace node_id with ip_address if possible
@router.post("/keep-alive")
async def keep_alive(request: NodeKeepAliveRequest) -> JSONResponse:
    async with RedisClient() as redis:
        await redis.hset(
            request.node_id,
            mapping={
                "last_keep_alive": request.timestamp,
            },
        )
        return JSONResponse(content={"Pool status updated successfully"})


@router.patch("/register")
async def register():
    timestamp = int(datetime.now().timestamp())
    node_id = round(timestamp + random.randint(0, 1000))

    async with RedisClient() as redis:
        await redis.hset(
            f"worker-{node_id}",
            mapping={
                "last_keep_alive": timestamp,
            },
        )
        return JSONResponse(content={"node_id": f"worker-{node_id}"})
