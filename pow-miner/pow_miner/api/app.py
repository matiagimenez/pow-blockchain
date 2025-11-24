from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from pow_miner.helpers import initialize_gpu_context, send_keep_alive
from pow_miner.services.task import TaskService
from pow_miner.utils import Scheduler, Settings

from .routes import base_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    initialize_gpu_context()
    Scheduler.add_cronjob(
        job=send_keep_alive,
        interval=Settings.KEEP_ALIVE_INTERVAL,
    )
    Scheduler.start()
    await TaskService().consume_tasks()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(base_router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
