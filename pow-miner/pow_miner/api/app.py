from contextlib import asynccontextmanager

from pow_miner.utils import Scheduler, Settings
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routes import base_router


@asynccontextmanager
async def lifespan():
    # Scheduler.add_cronjob(
    #     job=process_transactions_and_build_block,
    #     interval=Settings.BLOCK_CREATION_INTERVAL,
    # )
    # Scheduler.start()
    yield


app = FastAPI(lifespan=lifespan)  # type: ignore[arg-type]

app.include_router(base_router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
